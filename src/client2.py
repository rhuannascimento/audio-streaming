import socket
import pyaudio

CHUNK = 4096  
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def transmitir_audio(sala, server_ip, server_port):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Transmitindo áudio para a sala '{sala}'...")

    sala_encoded = sala.encode()
    sala_len = len(sala_encoded)
    header = f"{sala_len:04d}".encode() + sala_encoded  

    try:
        while True:
            data = stream.read(CHUNK)
            sock.sendto(header + data, (server_ip, server_port)) 
    except KeyboardInterrupt:
        print("Transmissão encerrada.")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        sock.close()

def receber_audio(sala, server_ip, server_port):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_ip, server_port)) 

    print(f"Conectado à sala '{sala}', aguardando transmissão...")

    try:
        while True:
            data, addr = sock.recvfrom(65535) 
            stream.write(data)
    except KeyboardInterrupt:
        print("Recepção encerrada.")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        sock.close()

def cliente(server_ip='127.0.0.1', server_port=5005):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    escolha = input("Digite '1' para criar uma sala, 'NOME_DA_SALA' para entrar em uma sala: ")

    if escolha == '1':
        nome_sala = input("Digite o nome da sala: ")
        sock.sendto(f"CRIAR {nome_sala}".encode(), (server_ip, server_port))
        transmitir_audio(nome_sala, server_ip, server_port)
    else:
        sock.sendto(f"ENTRAR {escolha}".encode(), (server_ip, server_port))
        receber_audio(escolha, server_ip, server_port)

cliente()
