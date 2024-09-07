import grpc
import proto.dfs_pb2 as pb2
import proto.dfs_pb2_grpc as pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.DFSStub(channel)

        # Pregunta inicial
        has_account = input("¿Ya tienes cuenta? (y/n): ").lower()

        if has_account == 'n':
            # Creación de nueva cuenta
            username = input("Elige un nombre de usuario: ")
            password = input("Elige una contraseña: ")
            create_response = stub.CreateUser(pb2.CreateUserRequest(username=username, password=password))
            print(create_response.message)

            if not create_response.success:
                return  # Si hay un error al crear el usuario, salir del cliente
        else:
            # Login
            username = input("Username: ")
            password = input("Password: ")
        
        login_response = stub.Login(pb2.LoginRequest(username=username, password=password))
        print(login_response.message)

        if login_response.success:
            while True:
                command = input(f"{username}@dfs> ")
                if command == "ls":
                    response = stub.ListDirectories(pb2.ListRequest(username=username))
                    print("Directories:", response.directories)
                elif command.startswith("mkdir"):
                    dir_name = command.split(" ")[1]
                    response = stub.MakeDirectory(pb2.MakeDirRequest(username=username, directory_name=dir_name))
                    print(response.message)
                elif command == "exit":
                    break

if __name__ == '__main__':
    run()

