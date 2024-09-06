import socket
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)


UDP_IP = "" 
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

print("Aguardando transmissão de áudio...")

try:
    while True:
        data, addr = sock.recvfrom(CHUNK * 2) 
      
        stream.write(data)
except KeyboardInterrupt:
    print("Recepção de áudio encerrada.")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()
