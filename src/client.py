import socket
import wave
import json

# Configurações do cliente
IP_SERVIDOR = "127.0.0.1"
PORTA_SERVIDOR = 12345
PORTA_CLIENTE = 54321
TAMANHO_BUFFER = 4096  # Aumentado para 4096 bytes

def cliente_udp():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente_socket.bind(("0.0.0.0", PORTA_CLIENTE))

    print(f"Cliente ouvindo na porta {PORTA_CLIENTE}")

    # Recebe a primeira mensagem que serão os metadados
    metadados, _ = cliente_socket.recvfrom(TAMANHO_BUFFER)
    
    # Verifica se a mensagem começa com a tag "META"
    if metadados.decode().startswith("META"):
        # Remove a tag "META" e converte para dicionário
        metadados = json.loads(metadados.decode()[4:])
    else:
        print("Erro: não foram recebidos metadados válidos.")
        return

    # Cria arquivo de saída para salvar o áudio
    with wave.open(f'output_cliente_{PORTA_CLIENTE}.wav', 'wb') as wav_file:
        wav_file.setnchannels(metadados['nchannels'])
        wav_file.setsampwidth(metadados['sampwidth'])
        wav_file.setframerate(metadados['framerate'])

        while True:
            dados, _ = cliente_socket.recvfrom(TAMANHO_BUFFER)
            if not dados:
                break
            wav_file.writeframes(dados)

    cliente_socket.close()
    print(f"Áudio recebido e salvo como output_cliente_{PORTA_CLIENTE}.wav")

cliente_udp()
