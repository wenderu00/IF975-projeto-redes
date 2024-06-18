import socket
import threading
import os

# Configuração do cliente
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024
MESSAGE_PATH = "user_message.txt"

# pra colocar o nome e a gente pode escolher se coloca uma mensagem ex :”Digite seu nome:”

# funções utilitárias

def generate_message_path(client_socket):
    return f"{client_socket.getsockname()[0]}_{client_socket.getsockname()[1]}_{MESSAGE_PATH}"

# funções principais
def receive_messages(client_socket):
    path = generate_message_path(client_socket)
    while True:
        try:
            data, client_address = client_socket.recvfrom(BUFFER_SIZE)
            with open(path, "wb") as file:
                while data != b"EOF":
                    file.write(data)
                    data, _ = client_socket.recvfrom(BUFFER_SIZE)

            with open(path, "r") as file:
                message = file.read()
            os.remove(path)
            print(message)
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break

def send_message(client_socket):
    path = generate_message_path(client_socket)
    while True:
        message = input()
        with open(path, "w") as file:
            file.write(message)
        with open(path, "rb") as file:
            while (chunck := file.read(1)):
                client_socket.sendto(chunck, (SERVER_IP, SERVER_PORT))
        client_socket.sendto(b"EOF", (SERVER_IP, SERVER_PORT))
        os.remove(path)
        #client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind do socket a uma porta local
    client_socket.bind(('0.0.0.0', 0))
    
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    send_message(client_socket)
    