import socket
import threading

BUFFER_SIZE = 1024

def receive_audio(client_id, server_ip, server_port, output_file):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(b"Conectando", (server_ip, server_port))  # Envia uma mensagem inicial para se conectar
    
    with open(output_file, 'wb') as file:
        while True:
            data, _ = client_socket.recvfrom(BUFFER_SIZE)
            if not data:
                break
            file.write(data)
    
    print(f"Cliente {client_id} terminou de receber áudio.")
    client_socket.close()

if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 12345
    
    # Criação de dois clientes
    threading.Thread(target=receive_audio, args=(1, SERVER_IP, SERVER_PORT, "cliente1_audio.wav")).start()
    threading.Thread(target=receive_audio, args=(2, SERVER_IP, SERVER_PORT, "cliente2_audio.wav")).start()
