import socket
import json

# Server configurations
SERVER_HOST = 'localhost'
SERVER_PORT = 5556


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# resolution choices to directory names
RESOLUTION_MAPPING = {
    '1': '240p',
    '2': '360p',
    '3': '480p',
    '4': '720p'
}

def initialize_client():
    
    user_name = input("Enter your name: ")
    public_key_pem = input("Enter your public key (in PEM format): ")
    send_message_to_server(f"JOIN:{user_name}:{public_key_pem}")

    while True:
        choice = input("Enter '1' to send a message, '2' to upload a video, '3' to list and play available videos, or '4' to exit: ")
        if choice == '1':
            # Send a text message to the server
            message = input("Enter your message: ")
            send_message_to_server(message)
        elif choice == '2':
            video_path = input("Enter the path of the video file: ")
            resolution = input("Choose resolution: 1) 240p, 2) 360p, 3) 480p, 4) 720p: ")
            upload_video_to_server(video_path, resolution)
        elif choice == '3':
          
            list_and_play_available_videos()
        elif choice == '4':
           
            print("Exit")
            break
        else:
            print("Invalid choice. Please enter '1', '2', '3', or '4'.")

def send_message_to_server(message):
    
    client_socket.send(message.encode())

def handle_received_message_from_server(message):
    if message.startswith("ENCRYPTED:"):
        # Handle encrypted messages
        _, sender_name, encrypted_message = message.split(":", 2)
        decrypted_message = decrypt_received_message(encrypted_message)
        print(f"Received encrypted message from {sender_name}: {decrypted_message}")
    else:
        print(message)

def decrypt_received_message(encrypted_message):
    # Decrypt an encrypted message using the user's private key
    private_key_pem = input("Enter your private key (in PEM format): ")
   
    pass

def receive_messages_from_server():
   
    while True:
        data = client_socket.recv(1024)
        if data:
            handle_received_message_from_server(data.decode())

def upload_video_to_server(video_path, resolution_choice):
    resolution_dir = RESOLUTION_MAPPING.get(resolution_choice)
    if resolution_dir:
        send_message_to_server(f"UPLOAD:{video_path}:{resolution_dir}")
        print(f"Uploaded video {video_path}")
    else:
        print("Invalid resolution choice.")

def list_and_play_available_videos():
    videos = receive_video_list_from_server()
    if videos:
        print("Available videos:")
        for i, video in enumerate(videos, 1):
            print(f"{i}. {video}")
        choice = int(input("Enter the number of the video you want to play: "))
        video_key = list(videos.keys())[choice - 1]
        resolution_choice = input("Choose resolution: 1) 240p, 2) 360p, 3) 480p, 4) 720p: ")
        resolution = RESOLUTION_MAPPING.get(resolution_choice)
        if resolution:
            play_selected_video(video_key, resolution)
        else:
            print("Invalid resolution choice.")
    else:
        print("No videos available.")

def receive_video_list_from_server():
   
    data = client_socket.recv(1024)
    if data:
        return json.loads(data.decode())
    else:
        return None

def play_selected_video(video_name, resolution):
    # Request the server to play a specific video at a certain resolution
    send_message_to_server(f"PLAY:{video_name}:{resolution}")

if __name__ == "__main__":
    # Start the client application
    initialize_client()
    receive_messages_from_server()
