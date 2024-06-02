
import pygame
from network import Network
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
# Initialize Pygame
pygame.init()
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
WINDOW_SIZE = 800
GRID_SIZE = 20

def redrawWindow(win, p, other_players):
    win.fill(WHITE)
    if p:
        p.draw(win)
        for player in other_players:
            player.draw(win)
    pygame.display.update()

def main():
    server_number = 0
    servers = []
    addr = input("Server ADDRESS:     ")
    n = Network(addr)
    print(n.server)
    p = n.getP()

    # Check if the player object is retrieved successfully
    if p:
        print("Connected to the server successfully.")
    else:
        pygame.quit()
        print(f"Unable to connect to the server - {n.server}:{n.port}")
        return

    # Constants for the window dimensions

    # Set up the display window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Client")
    run = True  # Assume this retrieves the initial player state
    clock = pygame.time.Clock()
    overworld_1 = pygame.mixer.Sound("./Music/BirdPeople.ogg")
    overworld_1.play(-1)
    while run:
        clock.tick(60)  # Cap the frame rate at 60 FPS
        try:
            if p:
                other_players = n.send(p)
        except Exception as e:
            print(f"Error: {e}")
            run = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if p:
            p.move()
            redrawWindow(win, p, other_players)

    pygame.quit()

main()
