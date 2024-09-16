import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import argparse

def decrypt_file(encrypted_file, decrypted_file, key):
    with open(encrypted_file, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    with open(decrypted_file, 'wb') as f:
        f.write(unpadded_data)

def decrypt_folder(folder_path, output_folder, key):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.enc'):
            decrypted_file = os.path.join(output_folder, filename[:-4])  # Remove the '.enc' suffix
            decrypt_file(file_path, decrypted_file, key)
            print(f"Decrypted file: {decrypted_file}")

def main():
    parser = argparse.ArgumentParser(description='Decrypt a folder.')
    parser.add_argument('input_folder', help='Path to the folder with encrypted files')
    parser.add_argument('key_file', help='Path to the key file')
    
    args = parser.parse_args()
    input_folder = args.input_folder
    key_file = args.key_file
    
    base_name = os.path.basename(input_folder)
    directory = os.path.dirname(input_folder)
    output_folder = os.path.join(directory, f'decrypted_{base_name}')
    
    with open(key_file, 'rb') as kf:
        key = kf.read()
    
    decrypt_folder(input_folder, output_folder, key)
    print(f"Folder decrypted successfully! Decrypted files are in: {output_folder}")

if __name__ == "__main__":
    main()
