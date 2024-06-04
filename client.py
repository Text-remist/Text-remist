import random
import socket
import threading
import json
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.165.145.1"
ADDR = (SERVER, PORT)
connected = False
connected_clients = {}

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start():
    global connected
    try:
        client.connect(ADDR)
        connected = True
    except ConnectionRefusedError:
        print("Server Down")
        connected = False

    print("[CLIENT] CONNECTING TO SERVER")

    def disconnect():
        global connected
        print("[CLIENT] DISCONNECTING FROM SERVER\n")
        try:
            client.send(DISCONNECT_MESSAGE.encode(FORMAT))
        except Exception:
            print("[CLIENT] SERVER CONNECTION FAILED")
        connected = False
    username = input("Enter Username: ")
    print(json.dumps(username))
    client.send(json.dumps(username).encode(FORMAT))
    while connected:
        time.sleep(0.01)
        try:
            msg = client.recv(HEADER).decode(FORMAT)
            if msg != DISCONNECT_MESSAGE:
                data = json.loads(msg)
                print("[CLIENT] Server Data Received")
                data['age'] = random.randint(0, 15)
                print("[CLIENT] New Data:", data)

                age_update_msg = {'age_update': data['age']}

                client.send(json.dumps(age_update_msg).encode(FORMAT))
                print("[CLIENT] Server Data Sent\n")
            else:
                connected = False
                disconnect()
                print("[CLIENT] REASON: BLOCKED")
                return 0
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return 0
        except WindowsError:
            connected = False
            disconnect()
        except ConnectionResetError:
            connected = False
            disconnect()
        except Exception as e:
            print(f"An error occurred: {e}")
        except KeyboardInterrupt:
            connected = False
            disconnect()

start()
