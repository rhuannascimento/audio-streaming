import socket
import pyaudio

CHUNK = 1024  
FORMAT = pyaudio.paInt16 
CHANNELS = 1 
RATE = 44100 

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

UDP_IP = '127.0.0.255'
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Transmitindo áudio...")

try:
    while True:
        data = stream.read(CHUNK)
        sock.sendto(data, (UDP_IP, UDP_PORT))
except KeyboardInterrupt:
    print("Transmissão encerrada.")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    sock.close()
