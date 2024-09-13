from concurrent import futures
import grpc
import proto.dfs_pb2 as pb2
import proto.dfs_pb2_grpc as pb2_grpc
from users import UserManager
from itertools import cycle

class NameNode(pb2_grpc.DFSServicer):
    def __init__(self):
        # Inicializamos el UserManager y el ciclo secuencial de DataNodes
        self.data_nodes = ["localhost:50052", "localhost:50053"]
        self.node_iterator = cycle(self.data_nodes)
        self.user_manager = UserManager()
        self.file_metadata = {}

    def GetDataNodesForFile(self, request, context):
        """Devuelve la lista de DataNodes para almacenar los bloques de un archivo."""
        data_nodes = []
        for _ in range(request.total_blocks):
            data_node_address = next(self.node_iterator)
            data_nodes.append(data_node_address)
        return pb2.GetDataNodesResponse(success=True, data_nodes=data_nodes)

    def RegisterFileMetadata(self, request, context):
        """Registra los metadatos del archivo y actualiza la estructura de directorios"""
        file_key = f"{request.directory}/{request.file_name}"
        if file_key not in self.file_metadata:
            self.file_metadata[file_key] = {
                "total_blocks": request.total_blocks,
                "blocks": {}
            }

        # Guardamos la ubicación de los bloques y los DataNodes correspondientes
        for block_id, data_node_address in enumerate(request.data_nodes):
            self.file_metadata[file_key]["blocks"][block_id] = {
                "node": data_node_address,
                "path": f"block_{block_id}"
            }

        # Agregamos el archivo a la estructura de directorios
        success, message = self.user_manager.add_file_to_directory(
            request.username,
            request.directory,
            request.file_name
        )
        return pb2.RegisterFileMetadataResponse(success=success, message=message)
        
    def GetFileInfo(self, request, context):
        """Devuelve la estructura de bloques y nodos donde está almacenado el archivo."""
        file_key = f"{request.directory}/{request.file_name}"
        if file_key in self.file_metadata:
            file_info = self.file_metadata[file_key]
            return pb2.GetFileInfoResponse(
                success=True,
                total_blocks=file_info["total_blocks"],
                blocks=[
                    pb2.BlockInfo(node=block["node"], path=block["path"])
                    for block in file_info["blocks"].values()
                ]
            )
        return pb2.GetFileInfoResponse(success=False, message="Archivo no encontrado")


    def RemoveFile(self, request, context):
        """Elimina un archivo de los metadatos y de la estructura de directorios"""
        file_key = f"{request.directory}/{request.file_name}"
        
        if file_key in self.file_metadata:
            # Eliminar el archivo de los metadatos
            del self.file_metadata[file_key]

            # Eliminar el archivo de la estructura de directorios
            success, message = self.user_manager.remove_file(request.username, request.directory, request.file_name)
            return pb2.RemoveFileResponse(success=success, message=message)
        else:
            return pb2.RemoveFileResponse(success=False, message="Archivo no encontrado")

    def Login(self, request, context):
        success, message = self.user_manager.authenticate(request.username, request.password)
        return pb2.LoginResponse(success=success, message=message)

    def CreateUser(self, request, context):
        success, message = self.user_manager.create_user(request.username, request.password)
        return pb2.CreateUserResponse(success=success, message=message)

    def ListDirectories(self, request, context):
        directories = self.user_manager.list_directories(request.username, request.current_directory)
        return pb2.ListResponse(directories=directories)

    def MakeDirectory(self, request, context):
        success, message = self.user_manager.make_directory(request.username, request.directory_name)
        return pb2.MakeDirResponse(success=success, message=message)

    def ChangeDirectory(self, request, context):
        success, new_directory, message = self.user_manager.change_directory(request.username, request.target_directory)
        return pb2.ChangeDirResponse(success=success, new_directory=new_directory, message=message)

    def RemoveDirectory(self, request, context):
        success, message = self.user_manager.remove_directory(request.username, request.directory_name)
        return pb2.RemoveDirResponse(success=success, message=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_DFSServicer_to_server(NameNode(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


