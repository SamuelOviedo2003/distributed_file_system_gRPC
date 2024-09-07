class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.directories = []

class UserManager:
    def __init__(self):
        self.users = {}
        # Usuarios predefinidos para pruebas
        self.users['admin'] = User('admin', 'password')

    def authenticate(self, username, password):
        if username in self.users and self.users[username].password == password:
            return True, "Login successful"
        return False, "Invalid username or password"

    def create_user(self, username, password):
        if username in self.users:
            return False, "Username already exists"
        self.users[username] = User(username, password)
        return True, f"User {username} created successfully"

    def list_directories(self, username):
        if username in self.users:
            return self.users[username].directories
        return []

    def make_directory(self, username, directory_name):
        if username in self.users:
            self.users[username].directories.append(directory_name)
            return True, f"Directory {directory_name} created successfully"
        return False, "User not found"

