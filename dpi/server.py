import socket
import sys
import time

def read_msg(conn):
    data = b""
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
        if b"\x1c\r" in data:
            break
    return data.strip(b"\x0b\x1c\r")

def build_ack(msg):
    try:
        msh = msg.decode().split("\r")[0].split("|")
        msg_type = msh[8]
        msg_id = msh[9]
    except Exception:
        msg_type = "UNKNOWN"
        msg_id = ""
    ts = time.strftime("%Y%m%d%H%M%S")
    ack = f"MSH|^~\\&|dpi|recv|eai|send|{ts}||ACK^{msg_type}|{msg_id}|P|2.3\rMSA|AA|{msg_id}\r"
    return ack.encode()

PORT = int(sys.argv[1])
print(f"{time.strftime('%F %T')} Listening on {PORT}", flush=True)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("0.0.0.0", PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"{time.strftime('%F %T')} Connection from {addr}", flush=True)
            message = read_msg(conn)
            print(f"{time.strftime('%F %T')} Message:\n{message.decode(errors='replace')}", flush=True)
            ack = b"\x0b" + build_ack(message) + b"\x1c\r"
            conn.sendall(ack)
            print(f"{time.strftime('%F %T')} Sent ACK", flush=True)
