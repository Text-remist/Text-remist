import pygame
import time
male_names = [
    "Alexander",
    "Benjamin",
    "William",
    "James",
    "Samuel",
    "Michael",
    "Ethan",
    "Daniel",
    "Matthew",
    "Jacob"
]
width = 800
height = 800
char = pygame.image.load("Caseoh_60x39.webp")
class Player():
    def __init__(self, x, y, width, height, color, username):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 20
        self.username = username
        self.last_move_time = 0  # Initialize the last move time
        self.cooldown = 0.2  # Cooldown period in seconds

    def draw(self, win):
        font = pygame.font.SysFont("Arial", 30)  # You can choose any font and size
        text_surface = font.render(self.username, True, (0, 0, 0))  # Render the username text with white color
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width // 2, self.y - 20)  # Position the text above the player
        pygame.draw.rect(win,self.color,self.rect)
        win.blit(text_surface, text_rect)  # Draw the username text
    def move(self):
        current_time = time.time()
        if current_time - self.last_move_time < self.cooldown:
            return  # Exit the method if still in cooldown period

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel
            self.last_move_time = current_time  # Update last move time

        if keys[pygame.K_RIGHT] and self.x < width - self.width:
            self.x += self.vel
            self.last_move_time = current_time  # Update last move time

        if keys[pygame.K_UP] and self.y > self.vel:
            self.y -= self.vel
            self.last_move_time = current_time  # Update last move time

        if keys[pygame.K_DOWN] and self.y < height - self.height:  # Correct the width to height for vertical movement
            self.y += self.vel
            self.last_move_time = current_time  # Update last move time

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)