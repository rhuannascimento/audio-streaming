import socket
import threading

CHUNK = 8192 * 2 
MAX_UDP_PACKET_SIZE = 65507  

class AudioServer:
    def __init__(self, host='0.0.0.0', port=5005):
        self.host = host
        self.port = port
        self.salas = {} 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))

    def criar_sala(self, nome_sala, addr):
        if nome_sala not in self.salas:
            self.salas[nome_sala] = []
            print(f"Sala '{nome_sala}' criada por {addr}")
        else:
            print(f"Sala '{nome_sala}' já existe.")

    def adicionar_cliente(self, nome_sala, addr):
        if nome_sala in self.salas:
            self.salas[nome_sala].append(addr)
            print(f"Cliente {addr} entrou na sala '{nome_sala}'")

    def distribuir_audio(self, nome_sala, data, addr_origem):
        if nome_sala in self.salas:
            for addr in self.salas[nome_sala]:
                if addr != addr_origem: 
                    self.server_socket.sendto(data, addr)

    def handle_client(self):
        while True:
            data, addr = self.server_socket.recvfrom(MAX_UDP_PACKET_SIZE) 

            if data.startswith(b"CRIAR"):
                nome_sala = data[6:].decode()
                self.criar_sala(nome_sala, addr)
            
            elif data.startswith(b"ENTRAR"):
                nome_sala = data[7:].decode()
                self.adicionar_cliente(nome_sala, addr)
            
            else:  
                nome_sala_len = int(data[:4].decode())
                nome_sala = data[4:4 + nome_sala_len].decode() 
                audio_data = data[4 + nome_sala_len:] 
                self.distribuir_audio(nome_sala, audio_data, addr)
    
    def iniciar(self):
        print("Servidor central iniciado...")
        threading.Thread(target=self.handle_client).start()

servidor = AudioServer()
servidor.iniciar()
