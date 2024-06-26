import socket
import pickle
class Network:
    def __init__(self, addr):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = addr # Server IP
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
    def server_ip(self):
        return self.server
    def getP(self):
        return self.p
    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))  # Increased buffer size to handle more data
        except socket.error as e:
            print(e)