import pygame
import os

CARD_TYPES = ["spades", "clubs", "diamonds", "hearts"]
CARD_NUMS = ["A", "02", "03", "04", "05", "06", "07", "08", "09", "10", "J", "Q", "K"]

# Size
CARD_WIDTH, CARD_HEIGHT = 150, 150

# Dict of card sorted by type
CARDS = {}
CARD_BACK = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'PNG', 'Cards', 'card_back.png')), (CARD_WIDTH, CARD_HEIGHT))

for card_type in CARD_TYPES:
    card_images = []
    for card_num in CARD_NUMS:
        cardname = f"card_{card_type}_{card_num}.png"
        card_image = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'PNG', 'Cards', cardname)), (CARD_WIDTH, CARD_HEIGHT))
        card_images.append(card_image)
    CARDS[card_type] = card_images



class Card:
    def __init__(self, type, num):
        self.type = type
        self.num = num
        self.image = CARDS[type][num]
        self.rect = self.image.get_rect()
        self.back_image = CARD_BACK

    def draw(self, win, x, y, back = False):
        if back:
            win.blit(self.back_image, (x, y))
            return
        win.blit(self.image, (x, y))

    def draw_play(self, win, x, y):
        image = pygame.transform.scale(self.image, (300, 300))
        win.blit(image, (x, y))

class Card_4(Card):
    def __init__(self, type, num):
        super().__init__(type, num)

    def block():
        pass

class Card_A(Card):
    def __init__(self, type, num):
        super().__init__(type, num)

class Card_J(Card):
    def __init__(self, type, num):
        super().__init__(type, num)

class Card_Q(Card):
    def __init__(self, type, num):
        super().__init__(type, num)

class Card_K(Card):
    def __init__(self, x, y, type, num):
        super().__init__(x, y, type, num)