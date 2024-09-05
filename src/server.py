import socket
import wave
import time
import json

# Configurações do servidor
IP_SERVIDOR = "0.0.0.0"
PORTA_SERVIDOR = 12345
TAMANHO_BUFFER = 1024  # Tamanho do bloco de dados enviado a cada pacote

def servidor_udp(caminho_arquivo_wav):
    with wave.open(caminho_arquivo_wav, 'rb') as wav_file:
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        servidor_socket.bind((IP_SERVIDOR, PORTA_SERVIDOR))
        
        print(f"Servidor ouvindo em {IP_SERVIDOR}:{PORTA_SERVIDOR}")

        # Metadados
        metadados = {
            'nchannels': wav_file.getnchannels(),
            'sampwidth': wav_file.getsampwidth(),
            'framerate': wav_file.getframerate(),
            'nframes': wav_file.getnframes()
        }
        
        # Compacta os metadados usando JSON e adiciona uma tag especial "META"
        metadados_json = "META" + json.dumps(metadados)
        
        for cliente in lista_clientes:
            servidor_socket.sendto(metadados_json.encode(), cliente)
        
        # Transmissão de áudio
        while True:
            dados = wav_file.readframes(TAMANHO_BUFFER)
            if not dados:
                break

            for cliente in lista_clientes:
                servidor_socket.sendto(dados, cliente)

            time.sleep(0.01)

    servidor_socket.close()
    print("Transmissão concluída.")

# Lista de clientes
lista_clientes = [("127.0.0.1", 54321)]

# Caminho do arquivo .wav
caminho_arquivo = "vasco.wav"

servidor_udp(caminho_arquivo)
