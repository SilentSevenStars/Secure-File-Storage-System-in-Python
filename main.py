import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from auth import Auth
from vault import Vault
import os
import json

class SecureFileVaultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Vault")
        self.root.geometry("1280x720")
        self.root.configure(bg="#343333")  # Set background color of window
        self.root.resizable(False, False)
        self.auth = Auth()
        self.vault = Vault()
        self.create_login_screen()

    def set_background(self, image_path):
        image = Image.open(image_path)
        self.bg_image = ImageTk.PhotoImage(image)
        bg_label = tk.Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0)

    def create_login_screen(self):
        self.clear_screen()
        self.set_background("image/vault.png")

        bg = "#343333"
        fg = "white"

        tk.Label(self.root, text="USERNAME", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=700, y=230)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bg="white")
        self.username_entry.place(x=700, y=260)

        tk.Label(self.root, text="PASSWORD", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=700, y=310)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), width=30, bg="white")
        self.password_entry.place(x=700, y=340)

        tk.Button(self.root, text="Log in", bg="#3cbcf3", fg="white", font=("Arial", 12, "bold"), command=self.login).place(x=700, y=390)
        tk.Button(self.root, text="Register", bg="#555", fg="white", font=("Arial", 12), command=self.create_register_screen).place(x=800, y=390)

    def create_register_screen(self):
        self.clear_screen()
        self.set_background("image/createaccount.png")

        bg = "#343333"
        fg = "white"

        tk.Label(self.root, text="NAME", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=700, y=180)
        self.name_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bg="white")
        self.name_entry.place(x=700, y=210)

        tk.Label(self.root, text="USERNAME", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=700, y=250)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=30, bg="white")
        self.username_entry.place(x=700, y=280)

        tk.Label(self.root, text="PASSWORD", bg=bg, fg=fg, font=("Arial", 12, "bold")).place(x=700, y=320)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), width=30, bg="white")
        self.password_entry.place(x=700, y=350)

        tk.Button(self.root, text="Sign Up", bg="#3cbcf3", fg="white", font=("Arial", 12, "bold"), command=self.register).place(x=700, y=400)
        tk.Button(self.root, text="Back", bg="#555", fg="white", font=("Arial", 12), command=self.create_login_screen).place(x=800, y=400)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Fields cannot be blank")
            return
        if self.auth.login(username, password):
            self.vault.log_action(username, "login")
            name = self.auth.get_name(username)
            self.create_vault_screen(name, username)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not name or not username or not password:
            messagebox.showerror("Error", "Fields cannot be blank")
            return
        if self.auth.register(username, password, name):
            messagebox.showinfo("Success", "User registered")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "User already exists")

    def create_vault_screen(self, name, username):
        self.clear_screen()
        self.root.configure(bg="#343333")  # Ensure vault background is correct

        # --- Top bar ---
        top_frame = tk.Frame(self.root, bg="#c4c4c4", height=120, width=1280)
        top_frame.place(x=0, y=0)

        # Profile image
        profile_img = Image.open("image/profile.png").resize((100, 100))
        self.profile_photo = ImageTk.PhotoImage(profile_img)
        profile_label = tk.Label(top_frame, image=self.profile_photo, bg="#c4c4c4")
        profile_label.place(x=20, y=10)

        # Name and username
        tk.Label(top_frame, text=name, font=("Arial", 12, "bold"), bg="#c4c4c4", fg="black").place(x=140, y=30)
        tk.Label(top_frame, text=username, font=("Arial", 10), bg="#c4c4c4", fg="black").place(x=140, y=60)

        # Logout button (right side)
        tk.Button(top_frame, text="Log out", bg="red", fg="white", font=("Arial", 10, "bold"),
                command=lambda: self.logout(username)).place(x=1150, y=40, width=100, height=40)

        # --- Vault main buttons ---
        tk.Button(self.root, text="Encrypt", bg="#3cbcf3", fg="black", font=("Arial", 12, "bold"),
                command=lambda: self.vault.encrypt_file_gui(username)).place(x=550, y=250, width=150, height=40)

        tk.Button(self.root, text="Decrypt", bg="#7cf379", fg="black", font=("Arial", 12, "bold"),
                command=lambda: self.vault.decrypt_file_gui(username)).place(x=550, y=310, width=150, height=40)


    def logout(self, username):
        self.vault.log_action(username, "logout")
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    os.makedirs("encrypted_files", exist_ok=True)
    root = tk.Tk()
    app = SecureFileVaultApp(root)
    root.mainloop()
