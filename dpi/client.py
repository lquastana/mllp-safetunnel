import socket, sys, time

HOST = sys.argv[1]
PORT = int(sys.argv[2])
FILE = sys.argv[3]

with open(FILE, 'rb') as f:
    msg = f.read()

framed = b'\x0b' + msg + b'\x1c\r'
print(f"{time.strftime('%F %T')} Connecting to {HOST}:{PORT}", flush=True)
with socket.create_connection((HOST, PORT)) as s:
    s.sendall(framed)
print(f"{time.strftime('%F %T')} Sent {FILE}", flush=True)
