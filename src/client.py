import socket
import socket

# Configurações do cliente
IP_SERVIDOR = "127.0.0.1"
PORTA_SERVIDOR = 12345
PORTA_CLIENTE = 54321
TAMANHO_BUFFER = 2048 * 2

def cliente_udp():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente_socket.sendto(b"opa", (IP_SERVIDOR, PORTA_SERVIDOR))
   
    try:
        while True:
            audio_data, _ = cliente_socket.recvfrom(TAMANHO_BUFFER)
            print(audio_data)
    finally:
        cliente_socket.close()


cliente_udp()



