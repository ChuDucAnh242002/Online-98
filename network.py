import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.104.234.136"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(8192*4).decode()
        except socket.error as e:
            print(e)
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads((self.client.recv(8192*4)))
        except socket.error as e:
            self.client.send(str.encode("delete game"))
            print("socket error 2")
            print(e)