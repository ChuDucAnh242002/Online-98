import pygame
import os

pygame.font.init()

FONT = pygame.font.SysFont('comicsans', 36)
FONT2 = pygame.font.SysFont('comicsans', 24)

# Color
BLUE = (0, 0, 255)

# Size
BUTTON_WIDTH, BUTTON_HEIGHT = 500, 125
BUTTON_WIDTH_2, BUTTON_HEIGHT_2 = 75, 75

# Image
BLUE_BUTTON_1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'UI', 'blue_button1.png')), (BUTTON_WIDTH, BUTTON_HEIGHT))
BLUE_BUTTON_2 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'UI', 'blue_button2.png')), (BUTTON_WIDTH_2, BUTTON_HEIGHT_2))
BLUE_BUTTON_3 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'UI', 'blue_button3.png')), (BUTTON_WIDTH_2, BUTTON_HEIGHT_2))
BLUE_BUTTON_4 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'UI', 'blue_button4.png')), (BUTTON_WIDTH_2, BUTTON_HEIGHT_2))

BLUE_BUTTON = [BLUE_BUTTON_1, BLUE_BUTTON_2, BLUE_BUTTON_3, BLUE_BUTTON_4]


class Button:
    def __init__(self, x, y, text, num):
        self.text = text
        self.image = BLUE_BUTTON[num]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, win, width = 1200, height = 750, middle = True):
        text = FONT2.render(self.text, 1, BLUE)
        if middle:
            win.blit(self.image, (width //2 - self.rect.width /2, height //2 - self.rect.height /2))
            win.blit(text, (width //2 - text.get_width() /2, height //2 - text.get_height() /2))
            return
        win.blit(self.image, (self.rect.x, self.rect.y))
        win.blit(text, (self.rect.x +15, self.rect.y +18))

    def click(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            return True
        return False
