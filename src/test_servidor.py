import socket
from servidor import create_server

ip = "127.0.0.1"
port = 12345
server = create_server(ip, port)

# create server tests
def test_create_server_return_socket():
    assert isinstance(server,socket.socket)

def test_create_server_has_correct_ip():
    assert server.getsockname()[0] == ip

def test_create_server_has_correct_port():
    assert server.getsockname()[1] == port
