import pygame
import os
import random

from card import Card, CARD_TYPES

# Size
DECK_WIDTH, DECK_HEIGHT = 300, 300

CARD_BACK = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'PNG', 'Cards', 'card_back.png')), (DECK_WIDTH, DECK_HEIGHT))

class Deck:
    def __init__(self, x, y):
        self.cards = self.init_cards()
        self.image = CARD_BACK
        self.x = x
        self.y = y

    def init_cards(self):
        cards = []
        for type in CARD_TYPES:
            for num in range(12):
                card = Card(type, num)
                cards.append(card)
        return cards

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def remove_card(self):
        self.cards.pop()

    def remove_deck(self):
        pass

    def shuffle(self):
        random.shuffle(self.cards)

    def reset(self):
        pass

    def reset_in_match(self):
        pass

    def get_lastcard(self):
        return self.cards[-1]