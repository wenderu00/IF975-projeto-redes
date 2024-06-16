import socket
import threading
import datetime
import re

# Configuração do servidor
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# Armazenar os clientes conectados
clients = {}

# Funções utilitárias
def format_message(message, client_address, clients):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    return f"{client_address[0]}:{client_address[1]}/~{clients[client_address]}: {message} {timestamp}"

def is_connect_command(message):
    return "hi, meu nome eh <" in message

def is_exit_command(message):
    return message == "bye"

def is_client_in_room(client_address, room_clients):
    return client_address in room_clients

def catch_username(message):
    return message[len("hi, meu nome eh <"):len(message)-1] 

def create_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    return server_socket

def send_message(message, server_socket, client_address):
    server_socket.sendto(message.encode(), client_address)

def new_user_connection_message(new_user):
    return f"<{new_user}> foi conectado a sala"

def user_logged_out_message(disconnected_user):
    return f"<{disconnected_user}> saiu da sala"

def connected_message():
    return "conectado"

def not_connected_message():
    return "você não está conectado.\npara conectar digite o seguinte comando: \"hi, meu nome eh <NOME_DE_USUARIO>\""

def disconnected_message():
    return "você foi desconectado"

def server_new_connection_message(client_address):
    return f"Novo cliente conectado: {client_address}"

def server_disconnected_user_message(client_address):
    return f"cliente desconectado: {client_address}"

def server_start_message(server_socket):
    return f"Servidor iniciado em {server_socket.getsockname()[0]}:{server_socket.getsockname()[1]}"

def notify_every_client(clients, message, server_socket):
    for client in clients:
        send_message(message, server_socket, client)

# Função principal
def start_server():
    server_socket = create_server(SERVER_IP, SERVER_PORT)
    print(server_start_message(server_socket))
 
    while True:
        message, client_address = server_socket.recvfrom(BUFFER_SIZE)
        decode_message = message.decode()
        if not is_client_in_room(client_address, clients) and is_connect_command(decode_message):
            username = catch_username(decode_message)
            print(server_new_connection_message(client_address))
            send_message(connected_message(), server_socket, client_address)
            notify_every_client(clients, new_user_connection_message(username), server_socket)
            clients[client_address] = username 
            
        elif not is_client_in_room(client_address, clients) and not is_connect_command(decode_message):
            send_message(not_connected_message(),server_socket, client_address)
            
        elif is_exit_command(decode_message):
            disconnected_user = clients[client_address]
            del clients[client_address]
            print(server_disconnected_user_message(client_address))
            send_message(disconnected_message(), server_socket, client_address)
            notify_every_client(clients, user_logged_out_message(disconnected_user),server_socket)

        else:
            formatted_message = format_message(decode_message, client_address, clients)
            notify_every_client(clients, formatted_message, server_socket)
            

if __name__ == "__main__":
  start_server()