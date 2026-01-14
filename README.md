![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
# Python Socket File Transfer System

A Python TCP client–server file transfer application implementing a custom application-layer protocol with handshake validation and fixed-length headers.
Supports basic file operations over raw sockets: **LIST**, **GET**, and **PUT**.


## Overview

This project demonstrates low-level network programming fundamentals using Python sockets, including:
- TCP client–server architecture
- Custom message framing using fixed-length headers
- Handshake-based protocol validation
- File upload and download over sockets
- Command-line client interaction
The goal of this project is to simulate how real application-layer protocols work on top of TCP.


## Features

- `LIST` — retrieve a list of files from the server directory
- `GET` — download an image file from the server
- `PUT` — upload an image file to the server
- Handshake validation (`OK` / `ER`) before data transfer
- Fixed-length header (8 bytes) to frame messages reliably
- Simple, readable CLI interface

## Architecture

`Client  <─── TCP ───>  Server`

The server listens on a specified port and handles one client request at a time.
The client sends a command, waits for a handshake response, and then proceeds with data transfer if permitted.


## Protocol Design

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


## Requirements
- Python 3.8 or higher
- No external libraries (Python standard library only)


## Installation
```bash
git clone https://github.com/minkong05/Socket-Transfer-App.git
cd Socket-Transfer-App
```


## How to Run

### Start the Server
```bash
python3 server.py 5000
```
### Run Client Commands

#### LIST files on server
```bash
python3 client.py localhost 5000 LIST
```

#### Upload a file
```bash
python3 client.py localhost 5000 PUT image.jpg
```

#### Download a file
```bash
python3 client.py localhost 5000 GET image.jpg
```


## Supported File Types
Only image files are accepted:
- `.jpg`
- `.jpeg`
- `.png`

This restriction is enforced on **both client and server** sides.


## Project Structure
```bash
Socket-Transfer-App/
├── server.py          # TCP server (LIST / GET / PUT handling)
├── client.py          # TCP client CLI
├── client/            # Client-side download/upload directory
├── server_files/      # Server-side file storage
├── example.png        # Example transferred file
├── .gitignore
└── README.md
```


## Design Highlights

- Uses fixed-size headers for safe message framing
- Prevents overwriting existing files
- Ensures file integrity during transfer
- Clear separation between client and server responsibilities
- Designed for local testing (`localhost` / `127.0.0.1`)


## Limitations

- No encryption (data sent in plain TCP)
- No authentication or access control
- Single-threaded server
- Localhost usage only


## Future Improvements

- Add encryption (TLS / SSL)
- Implement user authentication
- Support concurrent clients (threading or async)
- Add checksum validation
- Expand supported file types
- Add logging and configuration options



## Author

Built by **Kong Yu Min**  
University of Glasgow  
Python | Backend | Security-focused Learning Platform
