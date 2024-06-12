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

def conect_message(message):
    return "hi, meu nome eh <" in message

def exit_message(message):
    return message == "bye"

def is_client_in_room(client_address, room_clients):
    return client_address in room_clients

def catch_username(message):
    return message[len("hi, meu nome eh <"):len(message)-1] 

def create_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    return server_socket

# Função principal
def start_server():
    server_socket = create_server(SERVER_IP, SERVER_PORT)
    print(f"Servidor iniciado em {server_socket.getsockname()[0]}:{server_socket.getsockname()[1]}")

    while True:
        message, client_address = server_socket.recvfrom(BUFFER_SIZE)
        decode_message = message.decode()
        if not is_client_in_room(client_address, clients) and conect_message(decode_message):
            clients[client_address] = catch_username(decode_message)
            print(f"Novo cliente conectado: {client_address}")
            server_socket.sendto("conectado".encode(), client_address)
            for client in clients:
                if client != client_address:
                    server_socket.sendto(f"<{clients[client_address]}> foi conectado a sala".encode(), client)    
            
        elif not is_client_in_room(client_address, clients) and not conect_message(decode_message):
            server_socket.sendto("você não está conectado.\npara conectar digite o seguinte comando: \"hi, meu nome eh <NOME_DE_USUARIO>\"".encode(), client_address)

        elif exit_message(decode_message):
            disconected_user = clients[client_address]
            del clients[client_address]
            print(f"cliente desconectado: {client_address}")
            server_socket.sendto("você foi desconectado".encode(), client_address)
            for client in clients:
                server_socket.sendto(f"<{disconected_user}> saiu da sala".encode(), client)
            
        else:
            formatted_message = format_message(decode_message, client_address, clients)
            for client in clients:
                server_socket.sendto(formatted_message.encode(), client)
            

if __name__ == "__main__":
  start_server()