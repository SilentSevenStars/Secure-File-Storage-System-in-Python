import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from auth import Auth
from vault import Vault
import os

class SecureFileVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Vault")
        self.root.geometry("1280x720")
        self.root.configure(bg="#343333")
        self.root.resizable(False, False)
        self.auth = Auth()
        self.vault = Vault()
        self.create_login_screen()
        self.file_widgets = []
        self.selected_files = []

    def set_background(self, image_path):
        image = Image.open(image_path)
        self.bg_image = ImageTk.PhotoImage(image)
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()
        self.vault_logo = ImageTk.PhotoImage(Image.open("image/vault.png"))
        logo_label = tk.Label(self.root, image=self.vault_logo, bg="#343333")
        logo_label.place(x=103, y=67)

        bg = "#343333"
        fg = "white"

        # Log In Title
        tk.Label(self.root, text="Log In", bg=bg, fg="white", font=("Arial", 28, "bold")).place(x=700, y=160)

        # Username
        tk.Label(self.root, text="USERNAME", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=700, y=230)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bg="white")
        self.username_entry.place(x=700, y=260)

        # Password
        tk.Label(self.root, text="PASSWORD", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=700, y=310)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), width=30, bg="white")
        self.password_entry.place(x=700, y=340)

        # Log in Button (centered under password)
        tk.Button(self.root, text="Log in", bg="#3cbcf3", fg="white", font=("Arial", 12, "bold"),
                command=self.login).place(x=815, y=390)  # Adjust X to center under input

        # Sign up prompt below login button
        tk.Label(self.root, text="Doesn't have an account?", bg=bg, fg="white", font=("Arial", 14)).place(x=700, y=440)
        signup_link = tk.Label(self.root, text="Sign up", bg=bg, fg="white", font=("Arial", 14, "underline"), cursor="hand2")
        signup_link.place(x=920, y=440)
        signup_link.bind("<Button-1>", lambda e: self.create_register_screen())


    def create_register_screen(self):
        self.clear_screen()

        # Image placement
        self.register_image = ImageTk.PhotoImage(Image.open("image/createaccount.png"))
        logo_label = tk.Label(self.root, image=self.register_image, bg="#343333")
        logo_label.place(x=650, y=-31)

        bg = "#343333"
        fg = "white"

        # Title
        tk.Label(self.root, text="CREATE ACCOUNT", bg=bg, fg="white", font=("Arial", 24, "bold")).place(x=160, y=40)

        # Name
        tk.Label(self.root, text="NAME", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=160, y=100)
        self.name_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bg="white")
        self.name_entry.place(x=160, y=130)

        # Username
        tk.Label(self.root, text="USERNAME", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=160, y=170)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bg="white")
        self.username_entry.place(x=160, y=200)

        # Password
        tk.Label(self.root, text="PASSWORD", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=160, y=240)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), width=30, bg="white")
        self.password_entry.place(x=160, y=270)

        # Confirm Password
        tk.Label(self.root, text="CONFIRM PASSWORD", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=160, y=310)
        self.confirm_password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), width=30, bg="white")
        self.confirm_password_entry.place(x=160, y=340)

        # Sign Up Button
        tk.Button(self.root, text="Sign Up", bg="#3cbcf3", fg="white", font=("Arial", 12, "bold"),
                command=self.register).place(x=235, y=390)

        # Login Redirect Text - just below the Sign Up button
        login_text = tk.Label(self.root, text="Already have an account?", bg=bg, fg="white", font=("Arial", 14))
        login_text.place(x=120, y=440)

        login_link = tk.Label(self.root, text="log in", bg=bg, fg="white", font=("Arial", 14, "underline"), cursor="hand2")
        login_link.place(x=340, y=440)
        login_link.bind("<Button-1>", lambda e: self.create_login_screen())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        if self.auth.login(username, password):
            self.vault.log_action(username, "login")
            name = self.auth.get_name(username)
            self.create_vault_screen(name, username)
        else:
            messagebox.showerror("Error", "Username or Password are incorrect")

    def register(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        if not name or not username or not password or not confirm_password:
            messagebox.showerror("Error", "Fields cannot be blank")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords and Confirm Password do not match")
            return
        if self.auth.register(username, password, name):
            messagebox.showinfo("Success", "User registered")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "User already exists")

    def create_vault_screen(self, name, username):
        self.clear_screen()
        self.root.configure(bg="#343333")

        top_frame = tk.Frame(self.root, bg="#c4c4c4", height=120, width=1280)
        top_frame.place(x=0, y=0)

        profile_img = Image.open("image/profile.png").resize((100, 100))
        self.profile_photo = ImageTk.PhotoImage(profile_img)
        profile_label = tk.Label(top_frame, image=self.profile_photo, bg="#c4c4c4")
        profile_label.place(x=20, y=10)

        tk.Label(top_frame, text=name, font=("Arial", 12, "bold"), bg="#c4c4c4", fg="black").place(x=140, y=30)
        tk.Label(top_frame, text=username, font=("Arial", 10), bg="#c4c4c4", fg="black").place(x=140, y=60)

        tk.Button(top_frame, text="Log out", bg="red", fg="white", font=("Arial", 10, "bold"),
                  command=lambda: self.logout(username)).place(x=1150, y=40, width=100, height=40)

        tk.Button(self.root, text="Encrypt", bg="#3cbcf3", fg="black", font=("Arial", 12, "bold"),
                  command=lambda: self.create_encryption_screen(username)).place(x=550, y=250, width=150, height=40)

        tk.Button(self.root, text="Decrypt", bg="#7cf379", fg="black", font=("Arial", 12, "bold"),
                  command=lambda: self.create_decryption_screen(username)).place(x=550, y=310, width=150, height=40)

    def create_encryption_screen(self, username):
        self.clear_screen()
        self.root.configure(bg="#343333")
        self.selected_files = []
        self.file_widgets = []

        tk.Label(self.root, text="Encryption", font=("Arial", 20, "bold"),
                 bg="#343333", fg="white").pack(pady=30)

        self.files_frame = tk.Frame(self.root, bg="#343333")
        self.files_frame.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#343333")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Open file", bg="#f4ad47", fg="black", font=("Arial", 12, "bold"),
                  width=15, command=self.open_file).grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="Encrypt", bg="#3cbcf3", fg="black", font=("Arial", 12, "bold"),
                  width=15, command=lambda: self.encrypt_selected_files(username)).grid(row=0, column=1, padx=10)

        tk.Button(button_frame, text="Return", bg="red", fg="white", font=("Arial", 12, "bold"),
                  width=15, command=lambda: self.create_vault_screen(self.auth.get_name(username), username)).grid(row=0, column=2, padx=10)

    def create_decryption_screen(self, username):
        self.clear_screen()
        self.root.configure(bg="#343333")
        self.selected_files = []
        self.file_widgets = []

        tk.Label(self.root, text="Decryption", font=("Arial", 20, "bold"),
                 bg="#343333", fg="white").pack(pady=30)

        self.files_frame = tk.Frame(self.root, bg="#343333")
        self.files_frame.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#343333")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Open Encrypted File", bg="#f4ad47", fg="black", font=("Arial", 12, "bold"),
                  width=20, command=self.open_file).grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="Decrypt", bg="#7cf379", fg="black", font=("Arial", 12, "bold"),
                  width=20, command=lambda: self.decrypt_selected_files(username)).grid(row=0, column=1, padx=10)

        tk.Button(button_frame, text="Return", bg="red", fg="white", font=("Arial", 12, "bold"),
                  width=20, command=lambda: self.create_vault_screen(self.auth.get_name(username), username)).grid(row=0, column=2, padx=10)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path and file_path not in self.selected_files:
            self.selected_files.append(file_path)
            self.refresh_file_display()

    def refresh_file_display(self):
        for widget in self.file_widgets:
            widget.destroy()
        self.file_widgets = []

        for idx, path in enumerate(self.selected_files):
            file_frame = tk.Frame(self.files_frame, bg="#d3d3d3", pady=5, padx=10)
            file_frame.pack(pady=5)

            tk.Label(file_frame, text=os.path.basename(path), font=("Arial", 10), bg="#d3d3d3").pack(side=tk.LEFT)
            tk.Button(file_frame, text="X", bg="black", fg="white",
                      command=lambda i=idx: self.remove_file(i)).pack(side=tk.RIGHT)

            self.file_widgets.append(file_frame)

    def remove_file(self, index):
        if 0 <= index < len(self.selected_files):
            del self.selected_files[index]
            self.refresh_file_display()

    def encrypt_selected_files(self, username):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected.")
            return
        for path in self.selected_files:
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                encrypted = self.vault.fernet.encrypt(data)
                filename = os.path.basename(path)
                os.makedirs("encrypted_files", exist_ok=True)
                encrypted_path = os.path.join("encrypted_files", filename + ".enc")
                with open(encrypted_path, 'wb') as f:
                    f.write(encrypted)
                self.vault.log_action(username, "encrypt", filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to encrypt {path}: {str(e)}")
        messagebox.showinfo("Success", "All files encrypted successfully!")
        self.selected_files.clear()
        self.refresh_file_display()

    def decrypt_selected_files(self, username):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected.")
            return
        for path in self.selected_files:
            try:
                with open(path, 'rb') as f:
                    encrypted_data = f.read()
                decrypted = self.vault.fernet.decrypt(encrypted_data)
                filename = os.path.basename(path).replace(".enc", "")
                os.makedirs("decrypted_files", exist_ok=True)
                decrypted_path = os.path.join("decrypted_files", filename)
                with open(decrypted_path, 'wb') as f:
                    f.write(decrypted)
                self.vault.log_action(username, "decrypt", filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt {path}: {str(e)}")
        messagebox.showinfo("Success", "All files decrypted successfully!")
        self.selected_files.clear()
        self.refresh_file_display()

    def logout(self, username):
        self.vault.log_action(username, "logout")
        self.create_login_screen()

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    os.makedirs("encrypted_files", exist_ok=True)
    os.makedirs("decrypted_files", exist_ok=True)

    root = tk.Tk()
    app = SecureFileVaultApp(root)
    root.mainloop()
