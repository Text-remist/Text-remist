import pygame
import random
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
width = 1920
height = 960
char = pygame.image.load("Caseoh_60x39.webp")
class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3
        self.username = random.choice(male_names)
        self.isjump = False
        self.jumpcount = 10
    def draw(self, win):
        font = pygame.font.SysFont("Arial", 30)  # You can choose any font and size
        text_surface = font.render(self.username, True, (0, 0, 0))  # Render the username text with white color
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width // 2, self.y - 20)  # Position the text above the player
        win.blit(char, (self.x,self.y))  # Draw the player rectangle

        win.blit(text_surface, text_rect)  # Draw the username text
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > self.vel:
            self.x -= self.vel

        if keys[pygame.K_RIGHT] and self.x < width - self.width - self.vel:
            self.x += self.vel
        if not (self.isjump):
            if keys[pygame.K_UP] and self.y > self.vel:
                self.y -= self.vel

            if keys[pygame.K_DOWN] and self.y < height - self.height - self.vel:
                self.y += self.vel

            if keys[pygame.K_SPACE]:
                self.isjump = True
        else:
            if self.jumpcount >= -10:
                neg = 1
                if self.jumpcount < 0:
                    neg = -1
                self.y -= (self.jumpcount ** 2) * 0.5 * neg
                self.jumpcount -= 1

            else:
                self.isjump = False
                self.jumpcount = 10
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)