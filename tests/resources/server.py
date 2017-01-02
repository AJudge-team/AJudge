import socket


con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
DEFAULT_CONTAINER_PORT = 50000

server_address = ("0.0.0.0", DEFAULT_CONTAINER_PORT)
con.bind(server_address)

con.listen(1)
connection, client_address = con.accept()
try:
    data = connection.recv(1000)
    print("recv : " + data)
finally:
    connection.close()
