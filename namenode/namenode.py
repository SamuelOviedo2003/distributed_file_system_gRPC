from concurrent import futures
import grpc
import proto.dfs_pb2 as pb2
import proto.dfs_pb2_grpc as pb2_grpc
from users import UserManager
import random 

class NameNode(pb2_grpc.DFSServicer):
    def __init__(self):
        self.data_nodes = ["localhost:50052", "localhost:50053"]
        self.user_manager = UserManager()


    def SendBlock(self, request, context):
        """ Recibe un bloque del cliente y lo distribuye en un DataNode """
        # Elegimos un DataNode aleatorio para almacenar el bloque
        data_node_address = random.choice(self.data_nodes)

        # Conectamos con el DataNode y enviamos el bloque
        with grpc.insecure_channel(data_node_address) as channel:
            stub = pb2_grpc.DataNodeStub(channel)
            response = stub.StoreBlock(pb2.StoreBlockRequest(block_id=request.block_id, data=request.data))

        return pb2.SendBlockResponse(success=response.success, message=response.message)

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


