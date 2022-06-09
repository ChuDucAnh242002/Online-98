import pygame
import os

pygame.font.init()

FONT = pygame.font.SysFont('comicsans', 36)
FONT2 = pygame.font.SysFont('comicsans', 24)

# Color
BLUE = (0, 0, 255)

# Size
BUTTON_WIDTH, BUTTON_HEIGHT = 400, 100
BUTTON_WIDTH_2, BUTTON_HEIGHT_2 = 75, 75

# Image
BLUE_BUTTON_1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'UI', 'blue_button1.png')), (BUTTON_WIDTH, BUTTON_HEIGHT))
BLUE_BUTTON_2 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'UI', 'blue_button2.png')), (BUTTON_WIDTH_2, BUTTON_HEIGHT_2))
BLUE_BUTTON_3 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'UI', 'blue_button3.png')), (BUTTON_WIDTH_2, BUTTON_HEIGHT_2))

BLUE_BUTTON = [BLUE_BUTTON_1, BLUE_BUTTON_2, BLUE_BUTTON_3]


class Button:
    def __init__(self, x, y, text, num):
        self.text = text
        self.num = num
        self.rect = self.init_rect(x, y, num)

    def init_rect(self, x, y, num):
        if num == 0:
            return pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        else:
            return pygame.Rect(x, y, BUTTON_WIDTH_2, BUTTON_HEIGHT_2)

    def draw(self, win, width = 1200, height = 750, middle = True):
        text = FONT2.render(self.text, 1, BLUE)
        if middle:
            win.blit(BLUE_BUTTON[self.num], (width //2 - self.rect.width /2, height //2 - self.rect.height /2))
            win.blit(text, (width //2 - text.get_width() /2, height //2 - text.get_height() /2 -5))
            return
        win.blit(BLUE_BUTTON[self.num], (self.rect.x, self.rect.y))
        win.blit(text, (self.rect.x +15, self.rect.y +18))

    def click(self, pos):
        if self.rect.collidepoint(pos[0], pos[1]):
            return True
        return False
