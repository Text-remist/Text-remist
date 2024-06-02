import pygame
from network import Network
from player import Player

# Initialize Pygame
pygame.init()

def redrawWindow(win, player, other_players):
    win.fill((255, 255, 255))
    player.draw(win)
    for p in other_players:
        p.draw(win)
    pygame.display.update()

def main():
    server_number = 0
    n = Network()
    servers = []
    for server in n.server_list:
        addr = (server, n.port)

        connection_result = n.server_list_connect(addr)
        print(f"{server_number}. {server} | Connection result: {connection_result}")
        server_number+=1
    while True:
        try:
            # Prompt the user to choose a server
            server_choice = int(input("Which Server? "))
        except ValueError:
            print("Not an integer. Please enter a valid server choice.")
            continue

        # Check if the server choice is within the valid range
        if 0 <= server_choice < len(n.server_list):
            # Update the server IP address based on the user's choice
            n.server = n.server_list[server_choice]
            print(f"Connecting to {n.server}:{n.port}...")

            # Attempt to get the player object from the selected server
            p = n.getP()

            # Check if the player object is retrieved successfully
            if p:
                print("Connected to the server successfully.")
                break  # Exit the loop if the connection is successful
            else:
                pygame.quit()
                print(f"Unable to connect to the server - {n.server}:{n.port}")
                continue  # Continue to prompt the user for a server choice
        else:
            print("Invalid server choice. Please enter a valid server index.")

    # Constants for the window dimensions
    width = 500
    height = 500

    # Set up the display window
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Client")
    run = True  # Assume this retrieves the initial player state
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)  # Cap the frame rate at 60 FPS

        try:
            other_players = n.send(p)
        except Exception as e:
            print(f"Error: {e}")
            run = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        p.move()

        redrawWindow(win, p, other_players)

    pygame.quit()

main()
