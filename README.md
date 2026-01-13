# Python Socket File Transfer System

A lightweight client–server file transfer application built using **Python TCP sockets**.  
The system supports uploading and downloading image files, listing server directory contents, and uses a simple handshake protocol to validate requests before data transfer.

This project demonstrates low-level networking concepts, custom protocol design, and safe file handling using Python.


## Features

- **LIST** — retrieve a list of files from the server directory
- **GET** — download an image file from the server
- **PUT** — upload an image file to the server
- Handshake-based request validation (`OK` / `ER`)
- Fixed-length header protocol for reliable data transfer
- Server-side file existence and type checks
- TCP-based communication using Python sockets


## Supported File Types

Only image files are accepted:
- `.jpg`
- `.jpeg`
- `.png`

This restriction is enforced on **both client and server** sides.


## How It Works

### Protocol Overview

1. Client connects to the server via TCP
2. Client sends a command:
   - `LIST`
   - `GET|filename`
   - `PUT|filename`
3. Server performs a **handshake check**
   - Sends `OK` if request is valid
   - Sends `ER` if request is rejected
4. If approved, file data is transferred using:
   - **8-byte length header**
   - Followed by raw file bytes


## How to Run

### 1. Start the Server
```bash
python3 server.py <port>
python3 server.py 5000
python3 client.py <host> <port> <command> [filename]
python3 client.py localhost 5000 LIST
python3 client.py localhost 5000 PUT photo.jpg
python3 client.py localhost 5000 GET photo.jpg
```

### Project Structure
.
├── client.py      # Client-side command handling and file transfer
├── server.py      # Server-side request processing and storage
└── README.md

Technologies Used
	•	Python 3
	•	TCP sockets (socket)
	•	Binary file I/O
	•	Custom application-layer protocol
	•	Basic error handling and validation

⸻

Design Highlights
	•	Uses fixed-size headers for safe message framing
	•	Prevents overwriting existing files
	•	Ensures file integrity during transfer
	•	Clear separation between client and server responsibilities
	•	Designed for local testing (localhost / 127.0.0.1)

⸻

Limitations
	•	No encryption (data sent in plain TCP)
	•	No authentication or access control
	•	Single-threaded server
	•	Localhost usage only

⸻

Future Improvements
	•	Add encryption (TLS / SSL)
	•	Implement user authentication
	•	Support concurrent clients (threading or async)
	•	Add checksum validation
	•	Expand supported file types
	•	Add logging and configuration options

⸻

Author

Kong Yu Min
University of Glasgow
Computer Science
