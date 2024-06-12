import socket
from servidor import create_server, conect_message, catch_username  

# create server tests

ip = "127.0.0.1"
port = 12345
server = create_server(ip, port)

def test_create_server_return_socket():
    assert isinstance(server,socket.socket)

def test_create_server_has_correct_ip():
    assert server.getsockname()[0] == ip

def test_create_server_has_correct_port():
    assert server.getsockname()[1] == port

# conect message tests

valid_conect_message = "hi, meu nome eh <pedro>"
invalid_conect_message = "hi meu nome é pedro"

def test_conect_message_is_valid():
    assert conect_message(valid_conect_message)

def test_conect_message_is_invalid():
    assert not conect_message(invalid_conect_message)

# catch username tests
username = "pedro"
def test_catch_username():
    assert catch_username(valid_conect_message) == username