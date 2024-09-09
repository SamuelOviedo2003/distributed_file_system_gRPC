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

    def SendBlock(self, request, context):
        """Recibe un bloque del cliente y lo distribuye secuencialmente entre los DataNodes."""
        data_node_address = next(self.node_iterator)

        # Conectamos con el DataNode y enviamos el bloque
        with grpc.insecure_channel(data_node_address) as channel:
            stub = pb2_grpc.DataNodeStub(channel)
            response = stub.StoreBlock(pb2.StoreBlockRequest(block_id=request.block_id, data=request.data))

        # Guardar metadatos del archivo en file_metadata
        if response.success:
            file_key = f"{request.directory}/{request.file_name}"
            if file_key not in self.file_metadata:
                self.file_metadata[file_key] = {
                    "total_blocks": 0,
                    "blocks": {}
                }
            file_info = self.file_metadata[file_key]
            file_info["total_blocks"] += 1
            file_info["blocks"][request.block_id] = {
                "node": data_node_address,
                "path": f"block_{request.block_id}"
            }

            # Solo agregamos el archivo a la estructura de directorios al enviar el primer bloque
            if request.is_first_block:
                success, message = self.user_manager.add_file_to_directory(
                    request.username,
                    request.directory,
                    request.file_name
                )
                return pb2.SendBlockResponse(success=success, message=message)
            return pb2.SendBlockResponse(success=response.success, message="Bloque enviado correctamente.")
        
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
        """Llama a remove_file para eliminar un archivo lógicamente"""
        success, message = self.user_manager.remove_file(
            request.username,
            request.directory,
            request.file_name
        )
        return pb2.RemoveFileResponse(success=success, message=message)

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


