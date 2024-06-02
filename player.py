import pygame

class Player():
    def __init__(self, x, y, width, height, color, username):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3
        self.username = username

    def draw(self, win):
        font = pygame.font.SysFont("Arial", 30)  # You can choose any font and size
        text_surface = font.render(self.username, True, (0, 0, 0))  # Render the username text with white color
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width // 2, self.y - 20)  # Position the text above the player
        pygame.draw.rect(win, self.color, self.rect)  # Draw the player rectangle
        win.blit(text_surface, text_rect)  # Draw the username text
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
