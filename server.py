import socket
import time
from _thread import start_new_thread
from player import Player
import pickle
import json
with open("large_array.json", "r") as file:
    map_data = json.load(file)
# Define the dimensions of the array

# Server configuration
server = "10.0.0.154"
port = 5555
BLOCKSIZE = 20
# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))
    exit()

s.listen()
print("Waiting for a connection, Server Started")

# Initialize an empty list to store player objects
players = []


def threaded_client(conn, player_index):
    # Send both the player object and the map data to the client
    conn.send(pickle.dumps(players[player_index]))
    reply = ""

    while True:
        time.sleep(0.001)
        try:
            data = conn.recv(2048)
            if not data:
                print("Disconnected")
                break

            data = pickle.loads(data)
            players[player_index] = data

            # Reply with the current list of players
            reply = players[:player_index] + players[player_index + 1:]

            conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(f"Error: {e}")
            break

    print(f"Lost connection with player {player_index}")
    conn.close()
    # Remove the player from the list when they disconnect
    del players[player_index]
    # Adjust player indices
    for i in range(player_index, len(players)):
        start_new_thread(threaded_client, (players[i].conn, i))


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Add new player to the list
    username = f"Player {len(players) +1}"
    new_player = Player(0,0, BLOCKSIZE, BLOCKSIZE, (255, 0, 0), username)
    print(f"{new_player.username} has joined")
    time.sleep(1)
    players.append(new_player)
    print(players)
    start_new_thread(threaded_client, (conn, len(players) - 1))