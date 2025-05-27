import os
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
from datetime import datetime

class Vault:
    def __init__(self, key_file='.env', log_file='logs/vault_log.txt'):
        self.key_file = key_file
        self.log_file = log_file
        self.key = self.load_key()
        self.fernet = Fernet(self.key)

    def load_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        else:
            with open(self.key_file, 'rb') as f:
                key = f.read()
        return key

    def log_action(self, user, action, filename=""):
        with open(self.log_file, 'a') as f:
            f.write(f"{datetime.now()} - {user} - {action} - {filename}\n")

    def encrypt_file_gui(self, user):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as f:
                data = f.read()
            encrypted = self.fernet.encrypt(data)
            filename = os.path.basename(file_path)
            encrypted_path = os.path.join("encrypted_files", filename + ".enc")
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted)
            self.log_action(user, "encrypt", filename)
            messagebox.showinfo("Success", f"Encrypted and saved: {encrypted_path}")

    def decrypt_file_gui(self, user):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                decrypted = self.fernet.decrypt(data)
                filename = os.path.basename(file_path).replace(".enc", "")
                decrypted_path = os.path.join("encrypted_files", "DEC_" + filename)
                with open(decrypted_path, 'wb') as f:
                    f.write(decrypted)
                self.log_action(user, "decrypt", filename)
                messagebox.showinfo("Success", f"Decrypted and saved: {decrypted_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt: {str(e)}")