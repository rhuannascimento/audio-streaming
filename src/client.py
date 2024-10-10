import socket
import threading
import pyaudio
import time

CHUNK = 1024  
FORMAT = pyaudio.paInt16  
CHANNELS = 1 
RATE = 44100  

BUFFER_SIZE = 65535 

class UDPClient:
    def __init__(self, server_ip, server_port, room_name, mode="listen"):
        self.server_address = (server_ip, server_port)
        self.room_name = room_name
        self.mode = mode
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.audio = pyaudio.PyAudio()
        self.running = True

    def start(self):
        if self.mode == "transmit":
            self.transmit_audio()
        elif self.mode == "listen":
            self.listen_audio()

    def transmit_audio(self):
        self.client_socket.sendto(f"JOIN:{self.room_name}".encode(), self.server_address)
        print(f"Transmissor conectado à sala {self.room_name}")

        stream = self.audio.open(format=FORMAT,
                                 channels=CHANNELS,
                                 rate=RATE,
                                 input=True,
                                 frames_per_buffer=CHUNK)

        try:
            while self.running:
                audio_data = stream.read(CHUNK, exception_on_overflow=False)
                self.client_socket.sendto(audio_data, self.server_address)
        except Exception as e:
            print(f"Erro na transmissão: {e}")
        finally:
            self.stop(stream)

    def listen_audio(self):
        self.client_socket.sendto(f"JOIN:{self.room_name}".encode(), self.server_address)
        print(f"Ouvinte conectado à sala {self.room_name}")

        stream = self.audio.open(format=FORMAT,
                                 channels=CHANNELS,
                                 rate=RATE,
                                 output=True,
                                 frames_per_buffer=CHUNK)

        try:
            while self.running:
                data, _ = self.client_socket.recvfrom(BUFFER_SIZE)
                stream.write(data)
        except Exception as e:
            print(f"Erro na recepção: {e}")
        finally:
            self.stop(stream)

    def stop(self, stream):
        self.running = False
        self.client_socket.sendto(f"LEAVE:{self.room_name}".encode(), self.server_address)
        print(f"Desconectado da sala {self.room_name}")
        stream.stop_stream()
        stream.close()
        self.client_socket.close()
        self.audio.terminate()

def menu():
    print("Escolha uma opção:")
    print("1. Transmitir áudio")
    print("2. Ouvir áudio")

    choice = input("Digite o número da opção: ")
    if choice == "1":
        return "transmit"
    elif choice == "2":
        return "listen"
    else:
        print("Opção inválida")
        return menu()

if __name__ == "__main__":
    # server_ip = input("Digite o IP do servidor: ")
    # server_port = int(input("Digite a porta do servidor: "))
    server_ip = "172.20.10.2"
    server_port = 5000
    room_name = input("Digite o nome da sala: ")

    mode = menu()

    client = UDPClient(server_ip=server_ip, server_port=server_port, room_name=room_name, mode=mode)
    
    client_thread = threading.Thread(target=client.start)
    client_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nInterrompido! Finalizando o cliente...")
        client.running = False
        client_thread.join()
