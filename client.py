import random
import socket
import threading
import pickle
import time

HEADER = 50000
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
    username = input("Enter Username: ")
    if username == "quit":
        return 0
    else:
        try:
            client.connect(ADDR)
            connected = True
            print("[CLIENT] CONNECTING TO SERVER")
        except ConnectionRefusedError:
            print("Server Down")
            connected = False
        except OSError:
            print("Server Down")
            connected = False


        def disconnect():
            global connected
            print("[CLIENT] DISCONNECTING FROM SERVER\n")
            try:
                client.send(DISCONNECT_MESSAGE)
            except Exception:
                print("[CLIENT] SERVER CONNECTION FAILED")
            connected = False
        if connected:
            client.send(pickle.dumps(username))
        while connected:
            try:
                msg = client.recv(HEADER)
                if msg != DISCONNECT_MESSAGE:
                    data = pickle.loads(msg)
                    my_player = data["player"]
                    all_players = data["all_players"]

                    print(f"({my_player.x}, {my_player.y})")
                    if all_players is not None:
                        # Ensure all_players excludes my_player by comparing with unique attribute (e.g., username)
                        all_players = [player for player in all_players if hasattr(player, 'username') and player.username != my_player.username]
                        for player in all_players:
                            print(f"{player.username} is located at ({player.x}, {player.y})")

                    print("[CLIENT] Server Data Received")
                    new_player_data = {
                        "player_update": {"username": my_player.username, "x": my_player.x, "y": my_player.y}}
                    client.send(pickle.dumps(new_player_data))
                    print("[CLIENT] Client Data Sent")
                else:
                    connected = False
                    disconnect()
                    print("[CLIENT] REASON: BLOCKED")
                    return 0
            except pickle.PickleError as e:
                print(f"Failed to decode pickle: {e}")
                return 0
            except OSError:
                connected = False
                disconnect()
            except ConnectionResetError:
                connected = False
                disconnect()
            except KeyboardInterrupt:
                connected = False
                disconnect()

start()
