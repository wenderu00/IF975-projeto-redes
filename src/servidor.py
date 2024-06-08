import socket
import threading
import datetime

# Configuração do servidor
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# Armazenar os clientes conectados
clients = {}

def handle_client(client_socket, client_address):
    while True:
        try:
            message, client_address = client_socket.recvfrom(BUFFER_SIZE)
            if not message:
                break
            
            
            user_ip, user_port, user_name, timestamp, user_message = message.decode().split("~")

            
            formatted_message = f"{user_ip}:{user_port}/~{user_name}: {user_message} {timestamp}"

           
            for client in clients:
                client_socket.sendto(formatted_message.encode(), client)
                
        except Exception as e:
            print(f"Erro ao lidar com o cliente {client_address}: {e}")
            break

    # Aqui remove o cliente quando a conexão é perdida
    del clients[client_address]
    client_socket.close()

def create_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, port))
    return server_socket

def start_server():
    server_socket = create_server(SERVER_IP, SERVER_PORT)
    print(f"Servidor iniciado em {server_socket.getsockname()[0]}:{server_socket.getsockname()[1]}")

    while True:
        message, client_address = server_socket.recvfrom(BUFFER_SIZE)

        if client_address not in clients:
            clients[client_address] = client_address
            threading.Thread(target=handle_client, args=(server_socket, client_address)).start()
            print(f"Novo cliente conectado: {client_address}")

if __name__ == "__main__":
  start_server()