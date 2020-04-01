import socket
import sys

# ------CONSTANTS-------
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 42424))
print("Server is running")
s.listen(5)
clientsockets = []

def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            cmd = f"{len(cmd):<{HEADERSIZE}}" + cmd
            conn.send(str.encode(cmd))
            client_response = ""
            is_new = True
            while True:
                msg = conn.recv(16)
                if is_new:
                    try:
                        response_len = int(msg[:HEADERSIZE])
                    except ValueError:
                        continue
                    is_new = False
                client_response += msg.decode("utf-8")
                if len(client_response)-HEADERSIZE == response_len:
                    print(client_response[HEADERSIZE:], end="")
                    break


while True:
    clientsocket, address = s.accept()
    clientsockets.append(clientsocket)
    print(f"Connection from {address[0]}:{address[1]} has been established.")
    #msg = f"Hello {address[0]}"
    #msg = f"{len(msg):<{HEADERSIZE}}" + msg
    #clientsocket.send(bytes(msg, "utf-8"))
    send_commands(clientsocket)
    clientsocket.close()
