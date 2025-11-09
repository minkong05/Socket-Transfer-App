import sys, socket, os, struct

FORMAT = 'utf-8'
BYTES = 8
image_set = {".jpg", ".jpeg", ".png"}

def image_check(name):
    return os.path.splitext(name.lower())[1] in image_set

def recv_line(socket):
    line = b''
    while True:
        b = socket.recv(1)
        if not b or b == b'\n': break
        line += b
    return line.decode(FORMAT)    

def send_mes(conn, mes):
    mes = mes.encode(FORMAT)
    mes_length = len(mes)
    mes_length_in_bytes = mes_length.to_bytes(BYTES, 'big')

    mes = mes_length_in_bytes + mes
    conn.sendall(mes)

def do_handshake(conn, filename, method):
    method = method.upper()
    exists = os.path.isfile(filename)

    # File type check
    if not image_check(filename):
        print(f"[HANDSHAKE] Refused — invalid file type ({filename})")
        conn.sendall("ER\n".encode(FORMAT))
        return "ER\n"

    # PUT request
    if method == "PUT":
        if exists:
            print(f"[HANDSHAKE] PUT refused — file already exists ({filename})")
            conn.sendall("ER\n".encode(FORMAT))
            return "ER\n"
        else:
            print(f"[HANDSHAKE] PUT accepted — ready to receive {filename}")
            conn.sendall("OK\n".encode(FORMAT))
            return "OK\n"

    # GET request
    if method == "GET":
        if exists:
            print(f"[HANDSHAKE] GET accepted — ready to send {filename}")
            conn.sendall("OK\n".encode(FORMAT))
            return "OK\n"
        else:
            print(f"[HANDSHAKE] GET refused — file not found ({filename})")
            conn.sendall("ER\n".encode(FORMAT))
            return "ER\n"

    # Unknown Op
    print(f"[HANDSHAKE] Invalid operation ({method})")
    conn.sendall("ER\n".encode(FORMAT))
    return "ER\n"


def do_list(conn):
    items = os.listdir(".")     # ["server.py", "photo.png"]
    text = ("\n".join(items) + "\n") if items else b""

    send_mes(conn, text)
    print(f"[LIST] Directory listing sent successfully ({len(items)} items)")

def do_put(conn, filename):
    do_handshake(conn, filename, "PUT")

    size_header = b''
    while len(size_header) < BYTES:
        chunk = conn.recv(BYTES - len(size_header))
        if not chunk:
            print("[ERROR] Connection closed before receiving file size")
            return
        size_header += chunk

    size = int.from_bytes(size_header, 'big')
    print(f"[PUT] Expecting {size} bytes for {filename}")

    # Receive the file bytes and write to disk
    with open(filename, "xb") as f:  # 'xb' = binary + fail if file exists
        received = 0
        while received < size:
            chunk = conn.recv(min(64 * 1024, size - received))
            if not chunk:
                print("[ERROR] Connection closed mid-transfer")
                return
            f.write(chunk)
            received += len(chunk)

    print(f"[SUCCESS] Received {filename} ({received} bytes)")

def do_get(conn, filename,):
    resp = do_handshake(conn, filename, "GET")

    if image_check(filename) and resp == "OK\n":
        print(f"[GET] Preparing to send file: {filename}")

        with open(filename, "rb") as file:
            data = file.read()    # read entire image into bytes

        data_length = len(data)
        data_length_in_bytes = data_length.to_bytes(BYTES, "big")
        data = data_length_in_bytes + data

        conn.sendall(data)
        print(f"[SUCCESS] File sent successfully ({data_length} bytes): {filename}")

    elif resp == "ER\n":
        print("[ERROR] Handshake failed — server refused request.")


def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    line = recv_line(conn).strip()      #   line = "PUT|{filename}", "GET|{filename}", "LIST"
    parts = line.split("|")

    op = parts[0].upper()
    filename = parts[1].lower() if len(parts) > 1 else None

    if op == "LIST":
        do_list(conn)
    elif op == "PUT":
        do_put(conn, filename)
    elif op == "GET":
        do_get(conn, filename)
    else:
        print("[ERROR] Unknown operation. ")
    
    return
    

def main():
    if len(sys.argv) < 2:
        print("usage: python3 server.py <port>")
        return
    if len(sys.argv) == 2:
        HOST = '127.0.0.1'
        PORT = int(sys.argv[1])
        ADDR = (HOST,PORT)

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        print("[STARTING] Server is starting...")

        server.listen()
        print(f"[LISTENING] Server is listening on {HOST}:{PORT}\n")
        while True:
            conn, addr = server.accept()
            print(f"[ACTIVE CONNECTION] {addr}")
            handle_client(conn, addr)


if __name__ == "__main__":
    main()