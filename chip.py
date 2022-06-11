import pygame
import os

# Size
CHIP_WIDTH, CHIP_HEIGHT = 100, 100

# Image
CHIPBLACKWHITE_BORDER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'PNG', 'Chips', 'chipBlackWhite_border.png')))
CHIPBLUEWHITE_BORDER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'PNG', 'Chips', 'chipBlueWhite_border.png')))
CHIPGREENWHITE_BORDER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'PNG', 'Chips', 'chipGreenWhite_border.png')))
CHIPREDWHITE_BORDER = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'PNG', 'Chips', 'chipRedWhite_border.png')))

class Chip:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    