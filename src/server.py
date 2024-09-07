import socket
import threading

BUFFER_SIZE = 65535

class Room:
    def __init__(self):
        self.clients = [] 

    def add_client(self, address):
        if address not in self.clients:
            self.clients.append(address)

    def remove_client(self, address):
        if address in self.clients:
            self.clients.remove(address)

    def broadcast(self, data, sender_address, server_socket):
        for client in self.clients:
            if client != sender_address:
                server_socket.sendto(data, client)

class UDPServer:
    def __init__(self, host="0.0.0.0", port=5000):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rooms = {}  
        self.client_rooms = {}

    def start(self):
        self.server_socket.bind(self.server_address)
        print(f"Servidor UDP iniciado em {self.server_address}")

        while True:
            try:
                data, address = self.server_socket.recvfrom(BUFFER_SIZE)
                self.handle_packet(data, address)
            except Exception as e:
                print(f"Erro: {e}")

    def handle_packet(self, data, address):
        try:
            if data.startswith(b"JOIN") or data.startswith(b"LEAVE"):
                command, room_name = data.decode().split(":")
                if room_name not in self.rooms:
                    self.rooms[room_name] = Room()

                room = self.rooms[room_name]

                if command == "JOIN":
                    room.add_client(address)
                    self.client_rooms[address] = room_name
                    print(f"{address} entrou na sala {room_name}")
                elif command == "LEAVE":
                    room.remove_client(address)
                    if address in self.client_rooms:
                        del self.client_rooms[address]
                    print(f"{address} saiu da sala {room_name}")
            else:
                if address in self.client_rooms:  # Verifica se o cliente está associado a uma sala
                    room_name = self.client_rooms[address]
                    room = self.rooms[room_name]
                    room.broadcast(data, address, self.server_socket)
                else:
                    print(f"Cliente {address} enviou dados, mas não está em nenhuma sala.")
        except Exception as e:
            print(f"Erro ao manipular pacote: {e}")

if __name__ == "__main__":
    server = UDPServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
