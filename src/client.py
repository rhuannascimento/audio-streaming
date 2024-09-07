import socket
import threading
import pyaudio

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
            while True:
                audio_data = stream.read(CHUNK, exception_on_overflow=False)
                self.client_socket.sendto(audio_data, self.server_address)
        except KeyboardInterrupt:
            pass
        finally:
            self.client_socket.sendto(f"LEAVE:{self.room_name}".encode(), self.server_address)
            print(f"Transmissor desconectado da sala {self.room_name}")
            stream.stop_stream()
            stream.close()

    def listen_audio(self):
        self.client_socket.sendto(f"JOIN:{self.room_name}".encode(), self.server_address)
        print(f"Ouvinte conectado à sala {self.room_name}")

        stream = self.audio.open(format=FORMAT,
                                 channels=CHANNELS,
                                 rate=RATE,
                                 output=True,
                                 frames_per_buffer=CHUNK)

        try:
            while True:
                data, _ = self.client_socket.recvfrom(BUFFER_SIZE)
                stream.write(data)
        except KeyboardInterrupt:
            self.client_socket.sendto(f"LEAVE:{self.room_name}".encode(), self.server_address)
            print(f"Ouvinte desconectado da sala {self.room_name}")
            stream.stop_stream()
            stream.close()
            pass
        finally:
            self.client_socket.sendto(f"LEAVE:{self.room_name}".encode(), self.server_address)
            print(f"Ouvinte desconectado da sala {self.room_name}")
            stream.stop_stream()
            stream.close()

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
    server_ip = input("Digite o IP do servidor: ")
    server_port = int(input("Digite a porta do servidor: "))
    room_name = input("Digite o nome da sala: ")
    
    mode = menu()  

    client = UDPClient(server_ip=server_ip, server_port=server_port, room_name=room_name, mode=mode)
    client_thread = threading.Thread(target=client.start)
    client_thread.start()
