# Python Socket File Transfer

A simple file-transfer system built using Python sockets. Supports sending/receiving images, listing directory contents, and performing basic handshake validation between client and server.

## Features
- `LIST` — list items in the server directory
- `GET` — retrieve an image or file
- `PUT` — upload an image or file
- Handshake-based request validation
- Server-side error handling
- Works fully over TCP sockets

## How to run
1. Start the server
2. Run the client

## Project Structure
- `server.py`: Handles socket connections, handshake, commands, file transfer
- `client.py`: Sends commands and receives server responses
- `images/`: optional folder for testing image transfers

## Technologies Used
- Python 3
- TCP sockets
- Basic file I/O
- Simple protocol/handshake design

## Future Improvements
- Add encryption
- Add authentication
- Improve error handling
- Add GUI or web interface
