import random
import grpc
import proto.dfs_pb2_grpc as pb2_grpc
import proto.dfs_pb2 as pb2
from users import UserManager
from itertools import cycle
import logging
import threading
import time
import sys
import signal
import crc32c
from concurrent import futures


# Configuración para detener hilos de manera controlada
stop_event = threading.Event()

def signal_handler(sig, frame):
    """Maneja la interrupción (Ctrl + C) para detener los hilos correctamente."""
    print("Deteniendo el NameNode...")
    stop_event.set()  # Activa el evento para detener los hilos
    sys.exit(0)

# Registrar el manejador de señales
signal.signal(signal.SIGINT, signal_handler)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NameNode(pb2_grpc.DFSServicer):
    def __init__(self):
        # Inicializamos el UserManager y el ciclo secuencial de DataNodes
        self.data_nodes = ["localhost:50052", "localhost:50053", "localhost:50054", "localhost:50055"]
        logging.info("Initializing NameNode with data nodes: %s", self.data_nodes)
        self.node_iterator = cycle(self.data_nodes)
        self.user_manager = UserManager()
        self.file_metadata = {}
        
        # Inicializar los estados de los DataNodes
        self.data_nodes_status = {node: True for node in self.data_nodes}  # Estado de los DataNodes (True si están activos)
        self.data_nodes_last_heartbeat = {node: time.time() for node in self.data_nodes}  # Último heartbeat registrado
        self.failed_data_nodes = set()  # Para rastrear los DataNodes que han fallado

    def Heartbeat(self, request, context):
        """Actualizamos la hora del último heartbeat recibido."""
        self.data_nodes_status[request.data_node_address] = True
        self.data_nodes_last_heartbeat[request.data_node_address] = time.time()
        logging.info(f"Heartbeat recibido de {request.data_node_address}")
        return pb2.HeartbeatResponse(success=True)

    def monitor_data_nodes(self):
        """Monitorea los DataNodes para detectar fallos."""
        while not stop_event.is_set():  # Detener el hilo si se activa el evento stop_event
            current_time = time.time()
            for data_node, last_heartbeat in self.data_nodes_last_heartbeat.items():
                if data_node not in self.failed_data_nodes:  # Verificar solo nodos no marcados como fallidos
                    if current_time - last_heartbeat > 20:  # Si han pasado más de 20 segundos sin recibir heartbeat
                        logging.warning(f"DataNode {data_node} no responde (caído)!")
                        self.data_nodes_status[data_node] = False
                        # Iniciar proceso de replicación para archivos del DataNode caído
                        self.handle_datanode_failure(data_node)
            time.sleep(5)

    def handle_datanode_failure(self, failed_node):
        """
        Maneja la caída de un DataNode buscando los archivos en el nodo caído y replicando
        en otros DataNodes.
        """
        logging.info(f"Iniciando proceso de replicación para DataNode caído: {failed_node}")
        replication_successful = True  # Flag para indicar si todas las replicaciones fueron exitosas

        # Recorrer todos los archivos en los metadatos del NameNode
        for file_key, file_info in self.file_metadata.items():
            for block_id, block_info in file_info["blocks"].items():
                # Verificar si el DataNode caído contenía este bloque
                if block_info["node"] == failed_node or block_info["replication_node"] == failed_node:
                    logging.info(f"El bloque {block_id} del archivo {file_key} estaba en el DataNode {failed_node}")
                    
                    # Verificar cuál es el nodo de replicación y actuar en consecuencia
                    if block_info["node"] == failed_node:
                        node_to_replicate_from = block_info["replication_node"]
                    else:
                        node_to_replicate_from = block_info["node"]
                    
                    # Encontrar un nuevo DataNode activo para la replicación
                    new_replication_node = self.find_available_datanode([node_to_replicate_from, failed_node])
                    if new_replication_node:
                        logging.info(f"Solicitando replicación del bloque {block_id} del archivo {file_key} desde {node_to_replicate_from} a {new_replication_node}")
                        # Iniciar la replicación
                        success = self.replicate_block(node_to_replicate_from, new_replication_node, block_id, file_key)
                        if success:
                            # Actualizar los metadatos
                            if block_info["node"] == failed_node:
                                block_info["node"] = new_replication_node
                            else:
                                block_info["replication_node"] = new_replication_node
                            logging.info(f"Bloque {block_id} replicado correctamente desde {node_to_replicate_from} a {new_replication_node}")
                        else:
                            replication_successful = False  # Si alguna replicación falla, no eliminar el nodo caído
                            logging.error(f"Falló la replicación del bloque {block_id} del archivo {file_key}")
                    else:
                        logging.error(f"No se encontró un DataNode alternativo para replicar el bloque {block_id} del archivo {file_key}")
        
        if replication_successful:
            logging.info(f"DataNode {failed_node} ha sido replicado completamente. Eliminando de la lista de monitoreo.")
            self.failed_data_nodes.add(failed_node)  # Marcar el DataNode como replicado y caído, para dejar de monitorearlo

    def find_available_datanode(self, exclude_nodes):
        """
        Encuentra un DataNode disponible (activo) que no esté en la lista de nodos excluidos.
        """
        for node in self.data_nodes:
            if node not in exclude_nodes and self.data_nodes_status[node]:
                return node
        return None

    def replicate_block(self, source_node, target_node, block_id, file_key):
        """
        Envía una solicitud de replicación al DataNode que tiene una réplica válida de un bloque.
        """
        try:
            with grpc.insecure_channel(source_node) as channel:
                stub = pb2_grpc.DataNodeStub(channel)
                
                # Utilizar directamente el path almacenado en la metadata
                block_info = self.file_metadata[file_key]["blocks"][block_id]
                block_path = block_info["path"]  # Obtenemos el path directamente
                
                # Solicitar el bloque del DataNode de origen
                response = stub.ReadBlock(pb2.ReadBlockRequest(block_path=block_path))
                
                if response.success:
                    logging.info(f"Leído exitosamente el bloque {block_id} del archivo {file_key} desde {source_node}")

                    # Replicar el bloque al nuevo DataNode
                    with grpc.insecure_channel(target_node) as target_channel:
                        target_stub = pb2_grpc.DataNodeStub(target_channel)
                        replication_response = target_stub.StoreBlock(pb2.StoreBlockRequest(
                            block_id=block_id,
                            data=response.data,  # Datos leídos del bloque
                            username=block_path.split("_")[0],  # Extraer el nombre del usuario desde el path
                            file_name=block_path.split("_")[1],  # Extraer el nombre del archivo desde el path
                            replication_addrs="",  # Ningún DataNode adicional para replicar
                            checksum=crc32c.crc32c(response.data)  # Calcular el checksum del bloque
                        ))
                        
                        if replication_response.success:
                            logging.info(f"Bloque {block_id} replicado exitosamente desde {source_node} a {target_node}")
                            return True
                        else:
                            logging.error(f"Error al replicar bloque {block_id} desde {source_node} a {target_node}: {replication_response.message}")
                            return False
                else:
                    logging.error(f"Error al leer bloque {block_id} del archivo {file_key} desde {source_node}: {response.message}")
                    return False
        except Exception as e:
            logging.error(f"Error replicando bloque {block_id} desde {source_node} a {target_node}: {e}")
            return False

    def GetDataNodesForFile(self, request, context):
        """Devuelve la lista de DataNodes para almacenar los bloques de un archivo."""
        data_nodes = []
        replication_metadata=[]
        for _ in range(request.total_blocks):
            data_node_address = next(self.node_iterator)
            data_nodes.append(data_node_address)
            replication_data_node = random.choice(self.data_nodes)
            while data_node_address == replication_data_node:
                replication_data_node = random.choice(self.data_nodes)
            replication_metadata.append(replication_data_node)
        logging.info("DataNodes for file: %s", data_nodes)
        logging.info("Replication DataNodes for file: %s", replication_metadata)
        return pb2.GetDataNodesResponse(success=True, data_nodes=data_nodes, replication_metadata=replication_metadata)

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
                "replication_node": request.replication_data_nodes[block_id],
                "path": f"{request.username}_{request.file_name}_block_{block_id}"  # Formato correcto del bloque
            }

        # Agregamos el archivo a la estructura de directorios
        success, message = self.user_manager.add_file_to_directory(
            request.username,
            request.directory,
            request.file_name
        )
        logging.info("File metadata registered: %s", self.file_metadata)
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
    namenode = NameNode()
    
    # Iniciar el hilo que monitorea los DataNodes
    monitor_thread = threading.Thread(target=namenode.monitor_data_nodes)
    monitor_thread.start()

    pb2_grpc.add_DFSServicer_to_server(namenode, server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while not stop_event.is_set():  # Mantiene el servidor en ejecución hasta que se reciba Ctrl+C
            time.sleep(1)
    except KeyboardInterrupt:
        print("Recibida señal de interrupción, apagando el NameNode...")
    
    # Detener el servidor y esperar a que el hilo de monitoreo termine
    server.stop(0)
    monitor_thread.join()

if __name__ == '__main__':
    serve()
