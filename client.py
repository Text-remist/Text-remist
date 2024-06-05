import socket
import pyaudio
import pickle
import struct
# Constants
HEADER = 4000000  # Adjusted to a more reasonable size for a header
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.165.145.1"
ADDR = (SERVER, PORT)
# Create client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False

def start():
    global connected
    username = input("Enter Username: ")

    if username.lower() == "quit":
        return

    try:
        client.connect(ADDR)
        connected = True
        print("[CLIENT] CONNECTING TO SERVER")
    except (ConnectionRefusedError, OSError) as e:
        print(f"[CLIENT] Server Down: {e}")
        connected = False
        return

    def disconnect():
        global connected
        print("[CLIENT] DISCONNECTING FROM SERVER\n")
        try:
            client.send(pickle.dumps(DISCONNECT_MESSAGE))
        except Exception:
            print("[CLIENT] SERVER CONNECTION FAILED")
        connected = False

    if connected:
        try:
            client.send(pickle.dumps(username))
        except Exception as e:
            print(f"[CLIENT] Failed to send username: {e}")
            disconnect()
            return
    p = pyaudio.PyAudio()
    CHUNK = 1024
    stream = p.open(format=p.get_format_from_width(2),
                    channels=2,
                    rate=44100,
                    output=True,
                    frames_per_buffer=CHUNK)
    while connected:
        try:
            msg = client.recv(HEADER)
            if not msg:
                print("[CLIENT] Connection closed by the server")
                connected = False
                break

            if pickle.loads(msg) == DISCONNECT_MESSAGE:
                print("[CLIENT] REASON: BLOCKED")
                disconnect()
                break

            try:
                data = pickle.loads(msg)
            except pickle.UnpicklingError as e:
                print(f"[CLIENT] Failed to decode pickle: {e}")
                continue

            my_player = data["player"]
            all_players = data["all_players"]
            music_data = data["music_data"]
            data_b = b""
            payload_size = struct.calcsize("Q")
            while len(data_b) < payload_size:
                packet = music_data  # 4K
                if not packet: break
                data_b += packet
            packed_msg_size = data_b[:payload_size]
            data_b = data_b[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data_b) < msg_size:
                data_b += music_data
            frame_data = data_b[:msg_size]
            data_b = data_b[msg_size:]
            frame = pickle.loads(frame_data)

            #stream.write(frame) # Disabled since music is annoying
            print(f"({my_player.x}, {my_player.y})")
            if all_players is not None:
                all_players = [player for player in all_players if player.username != my_player.username]
                for player in all_players:
                    print(f"{player.username} is located at ({player.x}, {player.y})")

            print("[CLIENT] Server Data Received")
            new_player_data = {
                "player_update": {
                    "username": my_player.username,
                    "x": my_player.x,
                    "y": my_player.y
                }
            }
            client.send(pickle.dumps(new_player_data))
            print("[CLIENT] Client Data Sent")
        except (pickle.PickleError, OSError, ConnectionResetError) as e:
            print(f"[CLIENT] Connection error: {e}")
            connected = False
            disconnect()
        except Exception as e:
            print(f"[CLIENT] An unexpected error occurred: {e}")
        except KeyboardInterrupt:
            print("[CLIENT] Keyboard interrupt received. Disconnecting...")
            connected = False
            disconnect()

start()
