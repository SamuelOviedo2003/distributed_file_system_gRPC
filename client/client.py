import grpc
import proto.dfs_pb2 as pb2
import proto.dfs_pb2_grpc as pb2_grpc

def partition_file(file_path, block_size):
    """ Divide un archivo en bloques de tamaño fijo """
    blocks = []
    with open(file_path, 'rb') as file:
        block_num = 0
        while True:
            block = file.read(block_size)
            if not block:
                break
            blocks.append((block_num, block))
            block_num += 1
    return blocks

def run():
    current_directory = "/"
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.DFSStub(channel)

        has_account = input("¿Ya tienes cuenta? (y/n): ").lower()

        if has_account == 'n':
            username = input("Elige un nombre de usuario: ")
            password = input("Elige una contraseña: ")
            create_response = stub.CreateUser(pb2.CreateUserRequest(username=username, password=password))
            print(create_response.message)

            if not create_response.success:
                return
        else:
            username = input("Username: ")
            password = input("Password: ")
        
        login_response = stub.Login(pb2.LoginRequest(username=username, password=password))
        print(login_response.message)

        if login_response.success:
            while True:
                command = input(f"{username}@dfs:{current_directory}> ")

                if command.startswith("get"):
                    # Obtener información del archivo
                    file_name = command.split(" ")[1]
                    response = stub.GetFileInfo(pb2.GetFileInfoRequest(username=username, directory=current_directory, file_name=file_name))
                    if response.success:
                        file_data = b""
                        for block in response.blocks:
                            with grpc.insecure_channel(block.node) as block_channel:
                                block_stub = pb2_grpc.DataNodeStub(block_channel)
                                block_response = block_stub.ReadBlock(pb2.ReadBlockRequest(block_path=block.path))
                                if block_response.success:
                                    file_data += block_response.data
                                else:
                                    print(f"Error leyendo bloque: {block_response.message}")
                        # Guardar o mostrar el archivo
                        with open(f"{file_name}_reconstructed", 'wb') as f:
                            f.write(file_data)
                        print(f"Archivo {file_name} reconstruido correctamente.")
                    else:
                        print(response.message)

                elif command.startswith("send"):
                    # Obtener la ruta del archivo, el nombre del archivo y el directorio actual
                    file_path = command.split(" ")[1]
                    file_name = file_path.split("/")[-1]
                    
                    blocks = partition_file(file_path, 250)  # Tamaño de bloque = 250 bytes
                    is_first_block = True  # Indicador de que estamos enviando el primer bloque
                    
                    # Enviar bloques al NameNode, incluyendo el directorio actual
                    for block_num, block in blocks:
                        response = stub.SendBlock(pb2.SendBlockRequest(
                            username=username, 
                            directory=current_directory,  # Pasamos el directorio actual
                            file_name=file_name, 
                            block_id=block_num, 
                            data=block,
                            is_first_block=is_first_block))  # Indicamos si es el primer bloque
                        print(response.message)
                        is_first_block = False  # Después del primer bloque, lo desactivamos

                elif command.startswith("ls -l"):
                    # Mostrar información detallada del archivo
                    file_name = command.split(" ")[2]
                    response = stub.GetFileInfo(pb2.GetFileInfoRequest(username=username, directory=current_directory, file_name=file_name))
                    if response.success:
                        print(f"Archivo: {file_name}")
                        print(f"Total de bloques: {response.total_blocks}")
                        for block in response.blocks:
                            print(f"Bloque en {block.node}, ruta: {block.path}")
                    else:
                        print(response.message)

                elif command == "ls":
                    response = stub.ListDirectories(pb2.ListRequest(username=username, current_directory=current_directory))
                    print("Directories:", response.directories)

                elif command.startswith("mkdir"):
                    dir_name = command.split(" ")[1]
                    response = stub.MakeDirectory(pb2.MakeDirRequest(username=username, directory_name=f"{current_directory}/{dir_name}"))
                    print(response.message)

                elif command.startswith("cd"):
                    target_dir = command.split(" ")[1]
                    if target_dir == "..":
                        if current_directory != "/":
                            current_directory = "/".join(current_directory.split("/")[:-1])
                            if current_directory == "":
                                current_directory = "/"
                        print(f"Changed to directory {current_directory}")
                    else:
                        response = stub.ChangeDirectory(pb2.ChangeDirRequest(username=username, target_directory=f"{current_directory}/{target_dir}"))
                        if response.success:
                            current_directory = response.new_directory
                        print(response.message)

                elif command.startswith("rmdir"):
                    dir_name = command.split(" ")[1]
                    response = stub.RemoveDirectory(pb2.RemoveDirRequest(username=username, directory_name=f"{current_directory}/{dir_name}"))
                    print(response.message)

                elif command.startswith("rm"):
                    # Eliminar un archivo lógicamente
                    file_name = command.split(" ")[1]
                    response = stub.RemoveFile(pb2.RemoveFileRequest(username=username, directory=current_directory, file_name=file_name))
                    print(response.message)

                elif command == "exit":
                    break

if __name__ == '__main__':
    run()


