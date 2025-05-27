import argparse
import os
from cryptography.fernet import Fernet
from datetime import datetime

KEY_PATH = '.env'
LOG_PATH = 'logs/vault_log.txt'
ENCRYPTED_DIR = 'encrypted_files'

def load_key():
    with open(KEY_PATH, 'rb') as f:
        return f.read()

def log_action(action, filename):
    with open(LOG_PATH, 'a') as f:
        f.write(f"{datetime.now()} - batch - {action} - {filename}\n")

def process_folder(path, action):
    key = load_key()
    fernet = Fernet(key)

    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        if os.path.isfile(full_path):
            with open(full_path, 'rb') as f:
                data = f.read()

            if action == 'encrypt':
                result = fernet.encrypt(data)
                result_path = os.path.join(ENCRYPTED_DIR, filename + '.enc')
                log_action('encrypt', filename)
            else:
                try:
                    result = fernet.decrypt(data)
                    result_path = os.path.join(ENCRYPTED_DIR, 'DEC_' + filename.replace('.enc', ''))
                    log_action('decrypt', filename)
                except:
                    continue

            with open(result_path, 'wb') as f:
                f.write(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Folder path')
    parser.add_argument('action', choices=['encrypt', 'decrypt'])
    args = parser.parse_args()

    os.makedirs(ENCRYPTED_DIR, exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    process_folder(args.path, args.action)