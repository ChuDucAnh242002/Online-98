import pygame
import os

pygame.font.init()

FONT = pygame.font.SysFont('comicsans', 36)

# Color
BLUE = (0, 0, 255)

# Size
BUTTON_WIDTH, BUTTON_HEIGHT = 500, 125

# Image
BLUE_BUTTON = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'UI', 'blue_button1.png')), (BUTTON_WIDTH, BUTTON_HEIGHT))

class Button:
    def __init__(self, x, y, text):
        self.text = text
        self.image = BLUE_BUTTON
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, win, width = 1200, height = 750, middle = True):
        text = FONT.render(self.text, 1, BLUE)
        if middle:
            win.blit(self.image, (width //2 - self.rect.width /2, height //2 - self.rect.height /2))
            win.blit(text, (width //2 - text.get_width() /2, height //2 - text.get_height() /2))
            return
        win.blit(self, (self.rect.x, self.rect.y))

    def click(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            return True
        return False
