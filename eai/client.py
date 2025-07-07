import socket
import sys
import time

HOST = sys.argv[1]
PORT = int(sys.argv[2])
FILE = sys.argv[3]

with open(FILE, "rb") as f:
    msg = f.read()

framed = b"\x0b" + msg + b"\x1c\r"
ts = time.strftime("%F %T")
print(f"{ts} Connecting to {HOST}:{PORT}", flush=True)
with socket.create_connection((HOST, PORT)) as s:
    s.sendall(framed)
    print(f"{time.strftime('%F %T')} Sent {FILE}", flush=True)
    data = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
        if b"\x1c\r" in data:
            break

ack = data.strip(b"\x0b\x1c\r")
if ack:
    print(f"{time.strftime('%F %T')} Received ACK:\n{ack.decode(errors='replace')}", flush=True)
