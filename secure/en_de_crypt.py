"""
Description : A Python program to encrypt and decrypt files using AES encryption.
Location : https://github.com/sahuni/python
Date : 2024.12.20
"""
# pip install cryptography

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

def generate_key(password: str, salt: bytes) -> bytes:
    # Derive a cryptographic key from the password and salt using PBKDF2HMAC
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(file_path: str, password: str):
    # Generate a random salt
    salt = os.urandom(16)
    # Generate a key using the password and salt
    key = generate_key(password, salt)
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)
    # Create a Cipher object using the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    # Read the file data
    with open(file_path, 'rb') as f:
        data = f.read()

    # Pad the data to be a multiple of the block size
    padded_data = padder.update(data) + padder.finalize()
    # Encrypt the padded data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Write the salt, IV, and encrypted data to a new file
    with open(file_path + '.enc', 'wb') as f:
        f.write(salt + iv + encrypted_data)

def decrypt_file(file_path: str, password: str):
    # Read the salt, IV, and encrypted data from the file
    with open(file_path, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        encrypted_data = f.read()

    # Generate a key using the password and salt
    key = generate_key(password, salt)
    # Create a Cipher object using the key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    # Decrypt the data
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    # Remove the padding from the decrypted data
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    # Write the decrypted data to a new file
    with open(file_path.replace('.enc', ''), 'wb') as f:
        f.write(decrypted_data)

# encrypt_file('example.txt', 'your_password')
# decrypt_file('example.txt.enc', 'your_password')