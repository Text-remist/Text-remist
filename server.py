import random
import socket
import threading, wave, pyaudio,pickle,struct
import time
from pyfiglet import Figlet
from player import Player
import json

# Constants
BLOCKSIZE = 20
HEADER = 40000  # Adjusted to a more reasonable size for a header
PORT = 5050
SERVER = "192.165.145.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Load blocked list from JSON file
with open('blocked.json', 'r') as file2:
    BLOCKEDLIST_json = json.load(file2)

# Serialize the Python object and save it to a pickle file
with open('blocklist.pkl', 'wb') as file:
    pickle.dump(BLOCKEDLIST_json, file)

# Load the serialized object from the pickle file
with open('blocklist.pkl', 'rb') as file:
    BLOCKEDLST = pickle.load(file)
print(BLOCKEDLST)

# Global list to keep track of connected players
players = []

# Setup the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    global players
    connected = True

    # Initial check if the client's IP is blocked
    blocked = any(addr[0] == blocked_address for blocked_address in BLOCKEDLST)

    if blocked:
        print(f"[SERVER] CLIENT ({addr[0]}) IS ON BLOCKLIST\n[SERVER] DISCONNECTING BLOCKED CLIENT")
        conn.send(pickle.dumps(DISCONNECT_MESSAGE))
        conn.close()
        return

    # Read the initial username from the client
    try:
        username = pickle.loads(conn.recv(HEADER))
    except Exception as e:
        print(f"[ERROR] Error receiving username: {e}")
        conn.close()
        return

    # Add new player
    new_player = Player(0, 0, BLOCKSIZE, BLOCKSIZE, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), username)
    players.append(new_player)
    player_index = len(players) - 1

    print(f"[NEW CONNECTION] {addr} as {new_player.username}")
    CHUNK = 1024
    wf = wave.open("Persona.wav", 'rb')

    p = pyaudio.PyAudio()
    print('server listening at', (SERVER, (PORT - 1)))

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

    while connected:
        music_data = wf.readframes(CHUNK)
        music_data = pickle.dumps(music_data)
        music_data = struct.pack("Q", len(music_data)) + music_data
        try:
            # Prepare the data to send to the client
            all_players = [p for i, p in enumerate(players) if i != player_index]
            server_data = {"all_players": all_players, "player": new_player, "music_data": music_data}
            conn.send(pickle.dumps(server_data))

            # Receive data from the client
            received = conn.recv(HEADER)
            if received:
                if received == pickle.dumps(DISCONNECT_MESSAGE):
                    print(f"[CLIENT] {addr} DISCONNECTED")
                    connected = False
                else:
                    try:
                        received_data = pickle.loads(received)
                        if 'player_update' in received_data:
                            update = received_data['player_update']
                            for p in players:
                                if p.username == update['username']:
                                    p.x = update['x']
                                    p.y = update['y']
                    except Exception as e:
                        print(f"[ERROR] Error processing received data: {e}")
            else:
                connected = False

        except Exception as e:
            print(f"[ERROR] {e}")
            connected = False

    # Remove player when they disconnect
    print(f"[CLIENT] {addr} HAS DISCONNECTED")
    players.pop(player_index)
    conn.close()


def shutdown():
    print("\n[SERVER] DISCONNECTING CLIENT FROM SERVER\n")
    server.close()


def print_act_connections():
    while True:
        time.sleep(5)
        print(f"[ACTIVE CONNECTIONS] {len(players)}")


def start():
    server.listen()
    print(f"[SERVER] SERVER RUNNING ON {SERVER}")
    threading.Thread(target=print_act_connections).start()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


# Main entry point
f = Figlet(font='slant')
print(f.renderText('Online Server'))
print("[SERVER] SERVER IS STARTING")
start()
