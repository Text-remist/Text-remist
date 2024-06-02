import socket
import pickle
class Network:
    def __init__(self):
        self.server_list = ["10.0.0.154", "10.0.0.255", "10.0.0.189"]
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.0.0.154" # Server IP
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
    def server_ip(self):
        return self.server
    def getP(self):
        return self.p

    def server_list_connect(self, addr):
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.connect(addr)
            test_socket.close()  # Close the test socket immediately after connection
            return True  # Connection successful
        except Exception as e:
            return False  # Connection failed

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
