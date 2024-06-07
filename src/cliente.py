import socket
import threading
import datetime

# Configuração do cliente
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024
# pra colocar o nome e a gente pode escolher se coloca uma mensagem ex :”Digite seu nome:”
USER_NAME = input()

def receive_messages(client_socket):
    while True:
        try:
            message, server_address = client_socket.recvfrom(BUFFER_SIZE)
            if not message:
                break
            print(message.decode())
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break

def send_message(client_socket):
    while True:
        message = input()
        timestamp = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        formatted_message = f"{SERVER_IP}~ {SERVER_PORT}~ {USER_NAME}~ {timestamp}~{message}"
        client_socket.sendto(formatted_message.encode(), (SERVER_IP, SERVER_PORT))

if _name_ == "_main_":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(f"hi, meu nome eh {USER_NAME}".encode(), (SERVER_IP, SERVER_PORT))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    send_message(client_socket)