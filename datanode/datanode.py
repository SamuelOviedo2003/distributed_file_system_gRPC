import grpc
from concurrent import futures
import proto.dfs_pb2 as pb2
import proto.dfs_pb2_grpc as pb2_grpc
import os
import argparse

class DataNode(pb2_grpc.DataNodeServicer):
    def __init__(self, storage_dir):
        # Directorio donde se almacenarán los bloques
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def StoreBlock(self, request, context):
        """ Almacena un bloque en el DataNode """
        block_path = os.path.join(self.storage_dir, f"block_{request.block_id}")
        with open(block_path, 'wb') as block_file:
            block_file.write(request.data)
        return pb2.StoreBlockResponse(success=True, message=f"Block {request.block_id} stored successfully.")

    def ReadBlock(self, request, context):
        """Lee un bloque almacenado y lo devuelve al cliente"""
        block_path = os.path.join(self.storage_dir, request.block_path)
        if os.path.exists(block_path):
            with open(block_path, 'rb') as block_file:
                data = block_file.read()
            return pb2.ReadBlockResponse(success=True, data=data)
        return pb2.ReadBlockResponse(success=False, message="Bloque no encontrado")

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_DataNodeServicer_to_server(DataNode("data_storage"), server)
    server.add_insecure_port(f'[::]:{port}')  # El puerto es recibido como parámetro
    print(f"DataNode is listening on port {port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DataNode Server")
    parser.add_argument('--port', type=int, default=50052, help="Puerto en el que escuchará el DataNode")
    args = parser.parse_args()
    
    serve(args.port)
