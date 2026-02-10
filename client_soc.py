from Cryptodome.Cipher import ChaCha20
import socket
import os
import hashlib

os.system("clear")

# ASCII art banner
print(r""" ______ __  __  ______ __  __  ______  __   __      ______  ______  ______   
/\  == /\ \_\ \/\__  _/\ \_\ \/\  __ \/\ "-.\ \    /\  ___\/\  __ \/\  ___\  
\ \  _-\ \____ \/_/\ \\ \  __ \ \ \/\ \ \ \-.  \   \ \___  \ \ \/\ \ \ \____ 
 \ \_\  \/\_____\ \ \_\\ \_\ \_\ \_____\ \_\\"\_\   \/\_____\ \_____\ \_____\
  \/_/   \/_____/  \/_/ \/_/\/_/\/_____/\/_/ \/_/    \/_____/\/_____/\/_____/""")
# Connection settings
HOST = "127.0.0.1"

# Generate encryption keys
KEY = os.urandom(32)
NONCE = os.urandom(8)

file_list = None

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

# Choose connection type
message = input("\nSecure connection? (y/n)\n >> ")
if message == "y":
    PORT = 53189  # Secure port
else:
    PORT = 56723  # Unsecure port

# Create and connect socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Handle secure connection
if PORT == 53189:
    client.send(KEY)
    client.send(NONCE)
    file_list = decrypt_message(client.recv(1024), KEY, NONCE)

if file_list:
    # Display and handle file selection for secure connection
    i = 0
    for x in file_list.decode().split():
        i += 1
        print(f"[{i}] {x}")
    file_num = input("\nChoose a number to download: \n >> ")
    if file_num:
        client.send(encrypt_message(file_num.encode(), KEY, NONCE))

        hash = decrypt_message(client.recv(64), KEY, NONCE).decode()
        print(f"\n{hash}\n ")
        data = decrypt_message(client.recv(1024), KEY, NONCE).decode() 

        if get_hash(data.encode()) == hash:
            print("Checksum : Success!\n")
            print(data)
            if data:
                num = os.urandom(4).hex()
                os.system(f'echo "{data}" >> folder/download{num}.txt')
        else:
            print("\nChecksum : Failure!\n")        
else:
    # Handle unsecure connection
    file_list = client.recv(1024)
    
    if file_list:
        # Display and handle file selection for unsecure connection
        i = 0
        for x in file_list.decode().split():
            i += 1
            print(f"[{i}] {x}")
        file_num = input("\nChoose a number to download: \n >> ")
        if file_num:
            client.send(file_num.encode())
            
            data = client.recv(1024)
            print(data.decode())
            if data:
                num = os.urandom(4).hex()
                os.system(f'echo "{data}" >> download{num}.txt')
    else:
        print("Close connection")
        client.close()
