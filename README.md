# Secure-File-Storage-System-in-Python
# 🔐 Secure File Vault

A simple, secure file encryption/decryption vault with user authentication built using Python and Tkinter.

## 📦 Features

- User registration and login
- Encrypt and decrypt files securely using Fernet (AES)
- GUI with custom styling and images
- Logging of user actions (login, logout, encrypt, decrypt)
- File batch processing (via CLI option in `batch_processor.py`)

---

## 🖥️ GUI Demo

The app has a clean, intuitive interface with support for:
- Selecting files for encryption or decryption
- Account management
- Viewing user profile and logging out

---

## 🔧 Installation

1. Clone this repository:
https://github.com/SilentSevenStars/Secure-File-Storage-System-in-Python
2. On terminal:
pip install -r requirements.txt


## 🧭 Instructions
1. Registration
Click Register on the login screen.

Enter Name, Username, Password, and Confirm Password.

Click Sign Up to create an account.

![image alt](https://github.com/SilentSevenStars/Secure-File-Storage-System-in-Python/blob/main/image/register.png?raw=true)

2. Login
Enter your Username and Password.

Click Login to access the system.

![image alt](https://github.com/SilentSevenStars/Secure-File-Storage-System-in-Python/blob/main/image/login.png?raw=true)

3. Home Page
Shows your name and username.

Options:

Encrypt File – navigate to encryption page

Decrypt File – select and decrypt a .enc file

Logout – return to login page

![image alt](https://github.com/SilentSevenStars/Secure-File-Storage-System-in-Python/blob/main/image/homepage.png?raw=true)

4. Encrypt Page
Click Open File to select files.

Files are listed on screen with a remove (X) button.

Click Encrypt to encrypt all listed files.

Click Return to go back to home page.

![image alt](https://github.com/SilentSevenStars/Secure-File-Storage-System-in-Python/blob/main/image/encrypt.png?raw=true)

5. Decrypt Page
Click Open File and select encrypt files.

Files are listed on screen with a remove button.

Click Return to go back to home page.

![image alt](https://github.com/SilentSevenStars/Secure-File-Storage-System-in-Python/blob/main/image/decrypt.png?raw=true)

## 📝 Logs
All activities are recorded in logs/vault_log.txt including login/logout, encryption, and decryption actions with timestamps.

## 🔐 Encryption Details
Uses cryptography.fernet.Fernet for symmetric key encryption.

The encryption key is stored in .env file (auto-generated on first run).
