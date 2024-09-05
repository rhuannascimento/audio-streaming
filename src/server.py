import socket
import wave
import queue
import threading
import time

# Configurações do servidor
IP_SERVIDOR = "0.0.0.0"
PORTA_SERVIDOR = 12345
TAMANHO_BUFFER = 1024
TIMEOUT_ACK = 5  # Tempo máximo de espera por ACK em segundos

audio_queue = queue.Queue()

def handle_client(client_address, server_socket): 
    while True:
        try:
            data = audio_queue.get(timeout=1)
            if(data):
                server_socket.sendto(data, client_address)
        except queue.Empty:
            time.sleep(1)


def servidor_udp(caminho_arquivo_wav):
    with wave.open(caminho_arquivo_wav, 'rb') as wav_file:
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        servidor_socket.bind((IP_SERVIDOR, PORTA_SERVIDOR))
        
        print(f"Servidor ouvindo em {IP_SERVIDOR}:{PORTA_SERVIDOR}")

        while True:
            dados = wav_file.readframes(TAMANHO_BUFFER)
            audio_queue.put(dados)
            if not dados:
                break
            
            _, client_address = servidor_socket.recvfrom(TAMANHO_BUFFER)
            client_thread = threading.Thread(target=handle_client, args=(client_address, servidor_socket))
            client_thread.start()

            time.sleep(0.01)  # Pequeno atraso para evitar sobrecarga de pacotes

    servidor_socket.close()
    print("Transmissão concluída.")


# Caminho do arquivo .wav
caminho_arquivo = "vasco.wav"

servidor_udp(caminho_arquivo)



