import grpc
import proto.dfs_pb2 as pb2
import proto.dfs_pb2_grpc as pb2_grpc

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
                
                if command == "ls":
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

                elif command == "exit":
                    break

if __name__ == '__main__':
    run()


