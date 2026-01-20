import sys, socket, os, struct

FORMAT = 'utf-8'
BYTES = 8
image_set = {".jpg", ".jpeg", ".png"}

def image_check(name):
    return os.path.splitext(name.lower())[1] in image_set
    
def send_line(socket, line):
    socket.sendall((line + "\n").encode(FORMAT))     #   "PUT|{name}", "GET|{name}", "LIST"

def recv_mes(socket):
    def recv_all(amount_of_length):
        data = b''
        while len(data) < amount_of_length:
            chunk = socket.recv(amount_of_length - len(data))
            if not chunk:                           # peer closed early
                raise ConnectionError("Peer closed before all bytes were received")
            data += chunk
        return data

    data_length_in_bytes = recv_all(BYTES)
    data_length_int = int.from_bytes(data_length_in_bytes, 'big')

    data = recv_all(data_length_int)
    return data.decode(FORMAT)

def get_filename(pathname):
    return os.path.basename(pathname)
  
def handshake_check(socket):
    resp =  socket.recv(3).decode(FORMAT)
    if resp.startswith("OK"):
        print("→ Handshake successful — proceeding with transfer.")
        return True
    elif resp.startswith("ER"):
        print("→ Handshake failed — server rejected the request (invalid type or file state issue).")
        return False
    else :
        print("→ Handshake failed — unknown response from server.")
        return False


def to_put(host, port, filename):
    if image_check(filename) and os.path.isfile(filename):
        with open(filename, "rb") as file:
            data = file.read()    # read entire image into bytes

        data_length = len(data)
        data_length_in_bytes = data_length.to_bytes(BYTES, "big")
        data = data_length_in_bytes + data

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            ADDR = (host, port)

            c.connect(ADDR)
            send_line(c, f"PUT|{filename}")

            if handshake_check(c):
                c.sendall(data)
                print(f"→ {host}:{port} PUT {filename} -> success ({data_length} bytes)")
    else:
        print(f"→ {host}:{port} PUT {filename} -> failure (invalid file type or file not found)")

def to_get(host, port,filename):
    exists = os.path.isfile(filename)

    if image_check(filename) and not exists:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            ADDR = (host, port)
            c.connect(ADDR)
            
            send_line(c, f"GET|{filename}")

            if handshake_check(c):
                size_header = b''
                while len(size_header) < BYTES:
                    chunk = c.recv(BYTES - len(size_header))
                    if not chunk:
                        print("[ERROR] Connection closed before receiving file size")
                        return
                    size_header += chunk

                size = int.from_bytes(size_header, 'big')
                print(f"→ Expecting {size} bytes for {filename}")

                # Receive the file bytes and write to disk
                with open(filename, "xb") as f:  # 'xb' = binary + fail if file exists
                    received = 0
                    while received < size:
                        chunk = c.recv(min(64 * 1024, size - received))
                        if not chunk:
                            print("[ERROR] Connection closed mid-transfer")
                            return
                        f.write(chunk)
                        received += len(chunk)

                print(f"→ {host}:{port} PUT {filename} -> success ({size} bytes)")
    else:
        print(f"→ {host}:{port} GET {filename} -> failure (file already exists in client directory)")

def get_list(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:    #   c = client
        ADDR = (host, port)
        
        c.connect(ADDR)
        send_line(c, "LIST")
        data = recv_mes(c)

        print(f"→ {host}:{port} LIST -> success ({len(data.splitlines())} items)")
        for item in data.splitlines():
            print(f" - {item}")
        return


def main():
    usage = "usage: python3 client.py <host> <port> <put|get|list> [filename]"
    if len(sys.argv) < 4:
        print(usage)
        return
    HOST = sys.argv[1]
    try:
        PORT = int(sys.argv[2])
    except (ValueError):
        print("→ <port> must be a number")
        return
    op = sys.argv[3].upper()
    filename = None

    if HOST == "localhost" or HOST == "127.0.0.1":
        HOST = "127.0.0.1"
        print("→ Local host detected")
    else:
        print("→ Please try \"localhost\" or \"127.0.0.1\" ")
        return
    
    if op == "LIST" and len(sys.argv) == 4:
        get_list(HOST,PORT)
    

    elif op in ("GET", "PUT") and len(sys.argv) == 5:
        pathname = sys.argv[4].lower()
        filename = get_filename(pathname)

        if image_check(filename):
            if op == "PUT":
                to_put(HOST,PORT,filename)
            elif op == "GET":
                to_get(HOST,PORT,filename)
        else:
            print("→ invalid file type")
        
    else:
        print(usage)
        return

if __name__ == "__main__":
    main()