import socket
import threading

BUFFER_SIZE = 1024

def broadcast_audio(file_path, server_ip, server_port):

    
    print(f"Servidor pronto para transmitir no endereço {server_ip}:{server_port}")
    
    # Ler arquivo de áudio
    with open(file_path, 'rb') as audio_file:
        while True:
            data = audio_file.read(BUFFER_SIZE)
            if not data:
                break
            # Broadcast para os clientes conectados
            for client in clients:
                server_socket.sendto(data, client)
    
    print("Transmissão encerrada")
    server_socket.close()

# Lista de clientes conectados
clients = []

def handle_client(server_socket):
    while True:
        data, client_addr = server_socket.recvfrom(BUFFER_SIZE)
        if client_addr not in clients:
            clients.append(client_addr)
            print(f"Cliente {client_addr} conectado.")
        else:
            print(f"Dados recebidos de {client_addr}")

if __name__ == "__main__":
    SERVER_IP = "0.0.0.0"
    SERVER_PORT = 8080
    AUDIO_FILE = "vasco.wav"
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    
    # Thread para aceitar clientes
    threading.Thread(target=handle_client, args=(server_socket,), daemon=True).start()

    # Transmitir áudio
    broadcast_audio(AUDIO_FILE, SERVER_IP, SERVER_PORT)
