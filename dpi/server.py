import socket, sys, time

PORT = int(sys.argv[1])
print(f"{time.strftime('%F %T')} Listening on {PORT}", flush=True)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('0.0.0.0', PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"{time.strftime('%F %T')} Connection from {addr}", flush=True)
            data = b''
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b'\x1c\r' in data:
                    break
            message = data.strip(b'\x0b\x1c\r')
            print(f"{time.strftime('%F %T')} Message:\n{message.decode(errors='replace')}", flush=True)
