import hashlib
import os
import json

class Auth:
    def __init__(self, user_file='users.json'):
        self.user_file = user_file
        if not os.path.exists(self.user_file):
            with open(self.user_file, 'w') as f:
                json.dump({}, f)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        with open(self.user_file, 'r') as f:
            return json.load(f)

    def save_users(self, users):
        with open(self.user_file, 'w') as f:
            json.dump(users, f)

    def register(self, username, password, name):
        users = self.load_users()
        if username in users:
            return False
        users[username] = {
            "password": self.hash_password(password),
            "name": name
        }
        self.save_users(users)
        return True

    def login(self, username, password):
        users = self.load_users()
        return username in users and users[username]["password"] == self.hash_password(password)
    
    def get_name(self, username):
        users = self.load_users()
        return users[username]["name"] if username in users else "User"