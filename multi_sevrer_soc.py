from Cryptodome.Cipher import ChaCha20
import os
import socket
import threading
import hashlib


# Server configuration
HOST = "0.0.0.0"
PORT = (53189, 56723)  # Secure and unsecure ports

def get_hash(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data)
    return sha256_hash.hexdigest()

# Encryption/decryption functions
def encrypt_message(txt, key, nonce):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.encrypt(txt)

def decrypt_message(ciphertext, key, nonce):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.decrypt(ciphertext)

# File handling functions
def get_encoded_list(file_list):
    encoded_list = b'\n'.join(filename.encode() for filename in file_list)
    print(f"Encoded file list: {file_list}")
    return encoded_list

def get_encoded_file(file_list, index):
    index = int(index.decode()) - 1
    if 0 <= index < len(file_list):
        path ="storage/"+file_list[index]
        with open(path, 'rb') as f:
            return f.read()
    else:
        return b"Error: Invalid file index."

# Socket handling function
def get_soc(host, port):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind((host, port))
    soc.listen(5)
    
    print(f"Server is listening on {host}:{port}")
    while True:
        conn, addr = soc.accept()
        print(f"Server is connected to {addr}")
        
        # Handle secure connection
        if port == 53189:
            KEY = conn.recv(32)
            NONCE = conn.recv(8)
            print("the received key from client:", KEY.hex())

            conn.send(encrypt_message(get_encoded_list(file_list), KEY, NONCE))

            index = decrypt_message(conn.recv(1024), KEY, NONCE)
            print("Received from client:", index.decode())

            conn.send(encrypt_message(get_hash(get_encoded_file(file_list, index)).encode(), KEY, NONCE))

            conn.send(encrypt_message(get_encoded_file(file_list, index), KEY, NONCE))
        
        # Handle unsecure connection
        else:
            conn.send(get_encoded_list(file_list))

            index = conn.recv(1024)
            print("Received from client:", index.decode())

            conn.send(get_encoded_file(file_list, index))

# Get list of files in current directory
file_list = os.listdir("storage")

get_encoded_list(file_list)

# Start secure and unsecure server threads
threading.Thread(target=get_soc, args=(HOST, PORT[0])).start()
threading.Thread(target=get_soc, args=(HOST, PORT[1])).start()
