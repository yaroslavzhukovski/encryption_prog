from cryptography.fernet import Fernet
import os
import json

# File for storing key mappings
key_mapping_file = "key_mapping.json"

# Function to create a key
def create_key():
    return Fernet.generate_key()

# Function to save key mappings to a JSON file
def save_key_mapping(filename, key):
    # Load existing mappings
    mappings = load_key_mappings()
    mappings[filename] = key.decode()  # Store the key as a string
    # Save updated mappings
    with open(key_mapping_file, "w") as f:
        json.dump(mappings, f)

# Function to load key mappings from a JSON file
def load_key_mappings():
    if os.path.exists(key_mapping_file):
        with open(key_mapping_file, "r") as f:
            return json.load(f)
    return {}

# Function to encrypt a file
def encrypt_file():
    filename = input("Enter the filename to encrypt: ")
    if not os.path.exists(filename):
        print("File not found. Please ensure the filename is correct.")
        return

    key = create_key()  # Create a unique key for this file
    fernet = Fernet(key)
    
    with open(filename, "rb") as f:
        data = f.read()
    
    encrypted_data = fernet.encrypt(data)
    
    with open(filename + "_encrypted", "wb") as f:
        f.write(encrypted_data)

    save_key_mapping(filename, key)  # Save the key mapping
    print(f"File encrypted and saved as {filename}_encrypted")

# Function to decrypt a file
def decrypt_file():
    filename = input("Enter the filename to decrypt: ")
    if not os.path.exists(filename):
        print("File not found. Please ensure the filename is correct.")
        return

    # Load the key mapping
    mappings = load_key_mappings()
    original_filename = filename.replace("_encrypted", "")  # Get the original filename
    key_str = mappings.get(original_filename)

    if key_str is None:
        print(f"No key found for {original_filename}. Please ensure it has been encrypted.")
        return  # Exit if no key is found

    key = key_str.encode()  # Convert the key back to bytes
    fernet = Fernet(key)

    with open(filename, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(original_filename + "_decrypted", "wb") as f:
        f.write(decrypted_data)

    print(f"File decrypted and saved as {original_filename}_decrypted")

# Main function
def main():
    while True:
        action = input("Do you want to encrypt or decrypt a file? (encrypt/decrypt/exit): ").lower()
        
        if action == "encrypt":
            encrypt_file()
        elif action == "decrypt":
            decrypt_file()
        elif action == "exit":
            print("Thank you for using the program!")  # Thank you message
            break
        else:
            print("Invalid choice. Please enter 'encrypt', 'decrypt', or 'exit'.")

# Run the main function
main()
