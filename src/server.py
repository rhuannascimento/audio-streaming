import socket
import threading

CHUNK = 8192 * 2

class AudioServer:
    def __init__(self, host='0.0.0.0', port=5005):
        self.host = host
        self.port = port
        self.salas = {}  # Dicionário para armazenar salas e seus clientes
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
                    print(addr)
                    print(addr_origem)
                    self.server_socket.sendto(data, addr)



    def handle_client(self):
        while True:
            data, addr = self.server_socket.recvfrom(CHUNK)
            dataType, data = data.split()
            dataType = dataType.decode()


            if dataType.startswith("CRIAR"):
                nome_sala = data.decode()
                self.criar_sala(nome_sala, addr)
            elif dataType.startswith("ENTRAR"):
                nome_sala = data.decode()
                self.adicionar_cliente(nome_sala, addr)
            else:
                nome_sala = dataType.decode()
                self.distribuir_audio(nome_sala.decode(), data, addr)
    
    def iniciar(self):
        print("Servidor central iniciado...")
        threading.Thread(target=self.handle_client).start()

servidor = AudioServer()
servidor.iniciar()
