class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.directories = {"/": []}  # Estructura de directorios, comienza en la raíz "/"

class UserManager:
    def __init__(self):
        self.users = {}
        # Usuarios predefinidos para pruebas
        self.users['admin'] = User('admin', 'password')

    def add_file_to_directory(self, username, directory, file_name):
        """Agrega un archivo a la estructura de directorios lógica."""
        if username in self.users:
            user = self.users[username]
            # Verificar si el directorio existe
            if directory not in user.directories:
                user.directories[directory] = []
            # Agregar el archivo si no está ya presente
            if file_name not in user.directories[directory]:
                user.directories[directory].append(file_name)
                return True, f"Archivo {file_name} agregado correctamente a {directory}."
            else:
                return False, "El archivo ya existe en este directorio."
        return False, "Usuario no encontrado."

    def authenticate(self, username, password):
        if username in self.users and self.users[username].password == password:
            return True, "Login successful"
        return False, "Invalid username or password"

    def create_user(self, username, password):
        if username in self.users:
            return False, "Username already exists"
        self.users[username] = User(username, password)
        return True, f"User {username} created successfully"

    def list_directories(self, username, current_directory):
        """ Lista los directorios o archivos en el directorio actual """
        if username in self.users:
            user = self.users[username]
            if current_directory in user.directories:
                return user.directories[current_directory]  # Devolvemos los subdirectorios y archivos en el directorio actual
        return []

    def make_directory(self, username, directory_name):
        """ Crea un nuevo directorio dentro de otro """
        if username in self.users:
            user = self.users[username]
            parent_dir = "/".join(directory_name.split("/")[:-1])  # Directorio padre
            if parent_dir == "":
                parent_dir = "/"  # Si estamos en la raíz

            # Verificar si el directorio padre existe
            if parent_dir in user.directories:
                # Añadir el nuevo directorio
                if directory_name not in user.directories:
                    user.directories[directory_name] = []
                    user.directories[parent_dir].append(directory_name.split("/")[-1])  # Añadir el nuevo dir al padre
                    return True, f"Directory {directory_name} created successfully"
                return False, "Directory already exists"
            return False, "Parent directory not found"
        return False, "User not found"

    def change_directory(self, username, target_directory):
        """ Cambia el directorio actual """
        if username in self.users:
            user = self.users[username]
            if target_directory in user.directories:
                return True, target_directory, f"Changed to directory {target_directory}"
            return False, "/", "Directory not found"
        return False, "/", "User not found"

    def remove_directory(self, username, directory_name):
        """ Elimina un directorio si está vacío """
        if username in self.users:
            user = self.users[username]
            if directory_name in user.directories:
                if user.directories[directory_name] == []:  # Solo permite eliminar directorios vacíos
                    parent_dir = "/".join(directory_name.split("/")[:-1])  # Directorio padre
                    if parent_dir == "":
                        parent_dir = "/"
                    user.directories[parent_dir].remove(directory_name.split("/")[-1])  # Elimina del directorio padre
                    del user.directories[directory_name]  # Elimina el directorio
                    return True, f"Directory {directory_name} removed"
                return False, "Directory is not empty"
            return False, "Directory not found"
        return False, "User not found"
    
    def remove_file(self, username, directory, file_name):
        """Elimina un archivo de un directorio de manera lógica"""
        if username in self.users:
            user = self.users[username]
            
            # Verificar si el directorio existe
            if directory in user.directories:
                
                # Verificar si el archivo está en el directorio
                if file_name in user.directories[directory]:
                    user.directories[directory].remove(file_name)  # Elimina el archivo del directorio

                    
                    # También eliminamos el archivo de file_metadata
                    file_key = f"{directory}/{file_name}"
                    if file_key in user.file_metadata:
                        del user.file_metadata[file_key]
                        print("borrado de meta")
                    
                    return True, f"Archivo {file_name} eliminado correctamente de {directory}."
                else:
                    return False, "El archivo no se encuentra en este directorio."
            else:
                return False, "Directorio no encontrado."
        return False, "Usuario no encontrado."



