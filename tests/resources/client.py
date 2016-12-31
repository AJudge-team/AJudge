import socket
import sys


con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PAIR_PORT = 54321
server_address = ("0.0.0.0", PAIR_PORT)
con.connect(server_address)

try:
    message = "my message"
    con.sendall(message)
    data = con.recv(1000)
    print("from server : " + data)
finally:
    con.close()
