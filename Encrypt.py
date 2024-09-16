import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import argparse

def encrypt_file(input_file, output_file, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    with open(input_file, 'rb') as f:
        file_data = f.read()
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(file_data) + padder.finalize()
    
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    with open(output_file, 'wb') as f:
        f.write(iv + encrypted_data)

def encrypt_folder(folder_path, output_folder, key):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            encrypted_file = os.path.join(output_folder, f"{filename}.enc")
            encrypt_file(file_path, encrypted_file, key)
            print(f"Encrypted file: {encrypted_file}")

def main():
    parser = argparse.ArgumentParser(description='Encrypt a file or folder.')
    parser.add_argument('input_path', help='Path to the input file or folder')
    
    args = parser.parse_args()
    input_path = args.input_path

    key = os.urandom(32)  # Generate a random 256-bit key
    base_name = os.path.basename(input_path)
    directory = os.path.dirname(input_path)
    output_folder = os.path.join(directory, f'encrypted_{base_name}')
    
    key_file = os.path.join(directory, 'key.key')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    with open(key_file, 'wb') as kf:
        kf.write(key)
    
    if os.path.isfile(input_path):
        encrypted_file = os.path.join(output_folder, f"{os.path.basename(input_path)}.enc")
        encrypt_file(input_path, encrypted_file, key)
        print(f"File encrypted successfully! Encrypted file: {encrypted_file}, Key file: {key_file}")
    
    elif os.path.isdir(input_path):
        encrypt_folder(input_path, output_folder, key)
        print(f"Folder encrypted successfully! Encrypted files are in: {output_folder}, Key file: {key_file}")

if __name__ == "__main__":
    main()
