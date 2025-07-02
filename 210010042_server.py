import socket
import threading
import json
import os

# Server configurations
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 5556
VIDEO_UPLOAD_DIR = 'uploaded_videos'

active_clients = {}


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

#  resolution choices to directory names
RESOLUTION_OPTIONS = {
    '1': '240p',
    '2': '360p',
    '3': '480p',
    '4': '720p'
}

# List of available video files
VIDEO_DIRECTORY = "videos"

def handle_client_connection(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f"Client {client_address} disconnected")
                del active_clients[client_address]
                broadcast_active_clients()
                break
            message = data.decode()
            print(f"Received message from {client_address}: {message}")
            process_message(message, client_address, client_socket)
        except Exception as e:
            print("Error:", e)
            break

def process_message(message, client_address, client_socket):
    if message.startswith("JOIN"):
        _, username, public_key = message.split(":")
        active_clients[client_address] = (username, public_key, client_socket)
        broadcast_active_clients()
    elif message.startswith("SEND"):
        _, recipient_address, message_content = message.split(":", 2)
        sender_name = active_clients[client_address][0]
        encrypted_message = encrypt_message(message_content, active_clients[recipient_address][1])
        recipient_socket = active_clients[recipient_address][2]
        recipient_socket.send(f"ENCRYPTED:{sender_name}:{encrypted_message}".encode())
    elif message.startswith("UPLOAD"):
        _, video_path, resolution_choice = message.split(":")
        print(_, video_path, resolution_choice)
        upload_video_to_server(video_path, resolution_choice)
    elif message == "LIST":
        send_video_list_to_client(client_socket)
    elif message.startswith("PLAY"):
        video_name, resolution = message.split(":")[1], message.split(":")[2]
        play_video_for_client(client_socket, video_name, resolution)

def broadcast_active_clients():
    active_clients_dict = {str(address): (username, public_key) for address, (username, public_key, _) in active_clients.items()}
    message = json.dumps(active_clients_dict)
    for client_socket in active_clients.values():
        client_socket[2].send(message.encode())

def encrypt_message(message, public_key):
    pass

def upload_video_to_server(video_path, resolution_choice):
    print(f"Uploading video {video_path} with resolution {resolution_choice}")
    resolution_dir = resolution_choice
    if resolution_dir:
        resolution_dir_path = os.path.join(VIDEO_UPLOAD_DIR, resolution_dir)
        if not os.path.exists(resolution_dir_path):
            os.makedirs(resolution_dir_path)
        filename = os.path.basename(video_path)
        with open(video_path, 'rb') as file_to_upload:
            with open(os.path.join(resolution_dir_path, filename), 'wb') as uploaded_file:
                uploaded_file.write(file_to_upload.read())
        print(f"Uploaded video {filename}")
    else:
        print("Invalid resolution choice.")

def send_video_list_to_client(client_socket):
    videos = os.listdir(VIDEO_UPLOAD_DIR)
    client_socket.send(json.dumps(videos).encode())

def play_video_for_client(client_socket, video_name, resolution):
    # just print video_id, name and resolution
    video_path = os.path.join(VIDEO_UPLOAD_DIR, resolution, video_name)
    print(f"Playing video {video_path}")

def start_server():
    server_socket.listen()
    print(f"Server listening on {SERVER_ADDRESS}:{SERVER_PORT}")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
