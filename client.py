import pygame
from network import Network
from player import Player

# Initialize Pygame
pygame.init()

# Constants for the window dimensions
width = 500
height = 500

# Set up the display window
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

def redrawWindow(win, player, other_players):
    win.fill((255, 255, 255))
    player.draw(win)
    for p in other_players:
        p.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    p = n.getP()  # Assume this retrieves the initial player state
    if not p:
        print("Unable to connect to the server.")
        return

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
