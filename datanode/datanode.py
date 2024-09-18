import grpc
from concurrent import futures
import proto.dfs_pb2 as pb2
import proto.dfs_pb2_grpc as pb2_grpc
import os
import argparse
import crc32c
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataNode(pb2_grpc.DataNodeServicer):
    def __init__(self, storage_dir):
        # Directorio donde se almacenarán los bloques
        self.storage_dir = storage_dir
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def StoreBlock(self, request, context):
        """Almacena un bloque en el DataNode usando el formato nombreUsuario_nombreArchivo_blockid"""
        checksum_data_node = crc32c.crc32c(request.data)
        if checksum_data_node != request.checksum:
            return pb2.StoreBlockResponse(success=False, message="Checksums do not match. Failed Process.")
        block_path = os.path.join(self.storage_dir, f"{request.username}_{request.file_name}_block_{request.block_id}")
        logging.info(f"Saving {request.username}_{request.file_name}_block_{request.block_id}")
        with open(block_path, 'wb') as block_file:
            block_file.write(request.data)
        if request.replication_addrs == "": # Si no hay DataNode de replicación, se almacena el bloque en el DataNode actual
            return pb2.StoreBlockResponse(success=True, message=f"Block {request.block_id} stored successfully.")
        with grpc.insecure_channel(request.replication_addrs) as data_node_channel:
            data_stub = pb2_grpc.DataNodeStub(data_node_channel)
            data_response = data_stub.StoreBlock(pb2.StoreBlockRequest(
                block_id=request.block_id,
                data=request.data,
                username=request.username,
                file_name=request.file_name,  # Pasamos el nombre del archivo al DataNode
                replication_addrs="", # Pasamos la dirección del DataNode de replicación
                checksum=checksum_data_node
            ))
            logging.info(f"Replicating {request.username}_{request.file_name}_block_{request.block_id} to {request.replication_addrs}")
            success=data_response.success
        return pb2.StoreBlockResponse(success=success, message=data_response.message)

    def ReadBlock(self, request, context):
        """Lee un bloque almacenado y lo devuelve al cliente"""
        block_path = os.path.join(self.storage_dir, request.block_path)
        logging.info(f"Reading {request.block_path}")
        if os.path.exists(block_path):
            with open(block_path, 'rb') as block_file:
                data = block_file.read()
            return pb2.ReadBlockResponse(success=True, data=data)
        return pb2.ReadBlockResponse(success=False, message="Bloque no encontrado")

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_DataNodeServicer_to_server(DataNode(f"data_storage_{port}"), server)
    server.add_insecure_port(f'[::]:{port}')  # El puerto es recibido como parámetro
    logging.info(f"DataNode is listening on port {port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DataNode Server")
    parser.add_argument('--port', type=int, default=50052, help="Puerto en el que escuchará el DataNode")
    args = parser.parse_args()
    
    serve(args.port)
