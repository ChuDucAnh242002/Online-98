import pygame
import os

pygame.font.init()



# Size
CHIP_WIDTH, CHIP_HEIGHT = 75, 75

CHIP_TYPES = ["", "side"]
CHIP_COLORS = ["", "Red", "Blue", "Green", "Black"]

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
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def draw(self, win, x, y, num = 0):
        win.blit(CHIP[self.color][num], (x, y))
        
    def get_value(self):
        return self.value


# Stack for each kind of blind
class Stack:
    def __init__(self, id, blind):
        self.id = id
        self.chips = self.init_chips()
        self.blind = blind

    def init_chips(self):
        """
        return: Dict chips
        """
        chips = {}
        chips_white = []
        chips_red = []
        chips_blue = []
        chips_green = []
        chips_black = []
        # 1/2 blinds, 10 white, 10 red, 9, blue, 2 green
        if self.id == 0:
            for _ in range(10):
                chip_white = Chip("", 1)
                chip_red = Chip("Red", 5)
                chips_white.append(chip_white)
                chips_red.append(chip_red)
            for _ in range(9):
                chip_blue = Chip("Blue", 10)
                chips_blue.append(chip_blue)
            for _ in range(2):
                chip_green = Chip("Green", 25) 
                chips_green.append(chip_green)

            chips["White"] = chips_white
            chips["Red"] = chips_red
            chips["Blue"] = chips_blue
            chips["Green"] = chips_green

        # 2/5 blinds, 20 white, 16 red, 10 blue, 12 green
        elif self.id == 1:
            for _ in range(20):
                chip_white = Chip("", 1)
                chips_white.append(chip_white)
            for _ in range(16):
                chip_red = Chip("Red", 5)
                chips_red.append(chip_red)
            for _ in range(10):
                chip_blue = Chip("Blue", 10)
                chips_blue.append(chip_blue)
            for _ in range(12):
                chip_green = Chip("Green", 25)
                chips_green.append(chip_green)
            chips["White"] = chips_white
            chips["Red"] = chips_red
            chips["Blue"] = chips_blue
            chips["Green"] = chips_green

        # 5/10 blinds, 10 red, 10 blue, 10 green, 6 black
        elif self.id == 2:
            for _ in range(10):
                chip_red = Chip("Red", 5)
                chip_blue = Chip("Blue", 10)
                chip_green = Chip("Green", 25)
                chips_red.append(chip_red)
                chips_blue.append(chip_blue)
                chips_green.append(chip_green)
            for _ in range(6):
                chip_black = Chip("Black", 100)
                chips_black.append(chip_black)
                
            chips["Red"] = chips_red
            chips["Blue"] = chips_blue
            chips["Green"] = chips_green
            chips["Black"] = chips_black
        return chips
