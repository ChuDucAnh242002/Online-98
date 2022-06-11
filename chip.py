import pygame
import os

# Size
CHIP_WIDTH, CHIP_HEIGHT = 100, 100

CHIP_TYPES = ["", "side"]
CHIP_COLORS = ["Black", "Blue", "Green", "Red"]

# Image
CHIP = {}

for chip_color in CHIP_COLORS:
    chip_images = []
    for chip_type in CHIP_TYPES:
        chip_name = f"chip{chip_color}White_{chip_type}border.png"
        chip_image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'PNG', 'Chips', chip_name)), (CHIP_WIDTH, CHIP_HEIGHT))
        chip_images.append(chip_image)
    CHIP[chip_color] = chip_images

class Chip:
    def __init__(self, value):
        self.value = value

    def draw(self, win):
        pass
    
    def get_value(self):
        return self.value

    