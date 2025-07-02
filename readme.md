# Client-Server Video Messaging System

## Overview

This project consists of two Python scripts: one for the client-side and another for the server-side. The system enables users to send messages, upload videos, list available videos, and play videos of different resolutions over a TCP/IP network.

## Files

- **client.py**: This script contains the client-side implementation. It allows users to interact with the server by sending messages, uploading videos, and playing videos.
- **server.py**: This script contains the server-side implementation. It manages client connections, handles client requests, and facilitates video uploading and playback.

## Prerequisites

- Python 3.x
- Socket module (built-in)
- Threading module (built-in)

## Running the System

1. **Run the Server**: Execute the `server.py` script to start the server. The server will listen for incoming connections on `localhost` at port `5556`.

   ```bash
   python server.py
   ```

2. **Run the Client**: Execute the `client.py` script to start the client application. The client will connect to the server running on `localhost` at port `5556`.

   ```bash
   python client.py
   ```

3. **Interact with the Client**:
   - Upon running the client, you'll be prompted to enter your name and public key (in PEM format).
   - You can then choose to send a message, upload a video, or list and play available videos by entering the respective options.

## Message Encryption

- Messages sent between clients are encrypted to ensure privacy.
- The encryption and decryption logic is not implemented in the provided code but can be added in the `encrypt_message` and `decrypt_message` functions in both `client.py` and `server.py` scripts, respectively.

## Uploading and Playing Videos

- The client can upload videos of various resolutions to the server.
- Available videos can be listed and played by the client.
- Videos are stored in the `uploaded_videos` directory on the server.

## Contributing

Contributions to improve the functionality, efficiency, or documentation of this project are welcome. Please submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
