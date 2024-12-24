"""
Description : A Python program to manage passwords securely.
Location : https://github.com/sahuni/python
Date : 2024.12.24
"""
import hashlib
import os
import base64
from cryptography.fernet import Fernet

# Generate a key for encryption
def generate_key():
    return base64.urlsafe_b64encode(os.urandom(32))

# Encrypt the password
def encrypt_password(key, password):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

# Decrypt the password
def decrypt_password(key, encrypted_password):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()

# Hash the master password
def hash_master_password(master_password):
    return hashlib.sha256(master_password.encode()).hexdigest()

# Store the encrypted password
def store_password(service, encrypted_password):
    with open('passwords.txt', 'a') as file:
        file.write(f'{service}:{encrypted_password.decode()}\n')

# Retrieve the encrypted password
def retrieve_password(service):
    with open('passwords.txt', 'r') as file:
        for line in file:
            stored_service, stored_password = line.strip().split(':')
            if stored_service == service:
                return stored_password
    return None

def main():
    master_password = input("Enter the master password: ")
    hashed_master_password = hash_master_password(master_password)

    key = generate_key()

    while True:
        choice = input("Do you want to (1) store a new password or (2) retrieve a password? (1/2): ")
        if choice == '1':
            service = input("Enter the service name: ")
            password = input("Enter the password: ")
            encrypted_password = encrypt_password(key, password)
            store_password(service, encrypted_password)
            print("Password stored successfully.")
        elif choice == '2':
            service = input("Enter the service name: ")
            encrypted_password = retrieve_password(service)
            if encrypted_password:
                password = decrypt_password(key, encrypted_password.encode())
                print(f"The password for {service} is: {password}")
            else:
                print("Service not found.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()