import grpc
from concurrent import futures
import proto.dfs_pb2 as pb2
import proto.dfs_pb2_grpc as pb2_grpc
import os
import argparse
import crc32c
import logging
import threading
import time
import sys
import signal

# Configuración para detener hilos de manera controlada
stop_event = threading.Event()

def signal_handler(sig, frame):
    """Maneja la interrupción (Ctrl + C) para detener los hilos correctamente."""
    print("Deteniendo el servidor...")
    stop_event.set()  # Activa el evento para detener los hilos
    sys.exit(0)

# Registrar el manejador de señales
signal.signal(signal.SIGINT, signal_handler)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataNode(pb2_grpc.DataNodeServicer):
    def __init__(self, storage_dir, port, namenode_address):
        # Directorio donde se almacenarán los bloques
        self.storage_dir = storage_dir
        self.port = port  # Guarda el puerto en self.port
        self.namenode_address = namenode_address
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

    def send_heartbeat(self):
        """Envía un heartbeat al NameNode cada 5 segundos."""
        while not stop_event.is_set():  # Detener el hilo si se activa el evento stop_event
            try:
                with grpc.insecure_channel(self.namenode_address) as channel:
                    stub = pb2_grpc.DFSStub(channel)
                    response = stub.Heartbeat(pb2.HeartbeatRequest(data_node_address=f"localhost:{self.port}"))
                    if not response.success:
                        logging.warning(f"Heartbeat failed for DataNode {self.storage_dir}")
                    else:
                        logging.info(f"Heartbeat sent for DataNode {self.storage_dir}")
            except Exception as e:
                logging.error(f"Error sending heartbeat: {e}")
            time.sleep(10)  # Cada 5 segundos enviar el heartbeat

    def StoreBlock(self, request, context):
        """Almacena un bloque en el DataNode usando el formato nombreUsuario_nombreArchivo_blockid"""
        checksum_data_node = crc32c.crc32c(request.data)
        if checksum_data_node != request.checksum:
            return pb2.StoreBlockResponse(success=False, message="Checksums do not match. Failed Process.")
        block_path = os.path.join(self.storage_dir, f"{request.username}_{request.file_name}_block_{request.block_id}")
        logging.info(f"Saving {request.username}_{request.file_name}_block_{request.block_id}")
        with open(block_path, 'wb') as block_file:
            block_file.write(request.data)
        if request.replication_addrs == "":  # Si no hay DataNode de replicación, se almacena el bloque en el DataNode actual
            return pb2.StoreBlockResponse(success=True, message=f"Block {request.block_id} stored successfully.")
        with grpc.insecure_channel(request.replication_addrs) as data_node_channel:
            data_stub = pb2_grpc.DataNodeStub(data_node_channel)
            data_response = data_stub.StoreBlock(pb2.StoreBlockRequest(
                block_id=request.block_id,
                data=request.data,
                username=request.username,
                file_name=request.file_name,  # Pasamos el nombre del archivo al DataNode
                replication_addrs="",  # Pasamos la dirección del DataNode de replicación
                checksum=checksum_data_node
            ))
            logging.info(f"Replicating {request.username}_{request.file_name}_block_{request.block_id} to {request.replication_addrs}")
            success = data_response.success
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

def serve(port, namenode_address):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datanode = DataNode(f"data_storage_{port}", port, namenode_address)  # Pasa el puerto al constructor
    
    # Iniciar el hilo del heartbeat
    heartbeat_thread = threading.Thread(target=datanode.send_heartbeat)
    heartbeat_thread.start()

    pb2_grpc.add_DataNodeServicer_to_server(datanode, server)
    server.add_insecure_port(f'[::]:{port}')  # El puerto es recibido como parámetro
    logging.info(f"DataNode is listening on port {port}")
    server.start()

    try:
        while not stop_event.is_set():  # Mantiene el servidor en ejecución hasta que se reciba Ctrl+C
            time.sleep(1)
    except KeyboardInterrupt:
        print("Recibida señal de interrupción, apagando el DataNode...")
    
    # Cuando termine, detener el servidor y el hilo
    server.stop(0)
    heartbeat_thread.join()  # Asegura que el hilo se detenga antes de salir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DataNode Server")
    parser.add_argument('--port', type=int, default=50052, help="Puerto en el que escuchará el DataNode")
    parser.add_argument('--namenode_address', type=str, default="localhost:50051", help="Dirección del NameNode")
    args = parser.parse_args()
    
    serve(args.port, args.namenode_address)

