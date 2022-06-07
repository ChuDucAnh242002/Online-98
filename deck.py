import pygame
import os
import random

from card import Card, Card_4, Card_A_Heart, Card_A_Spades, Card_J, Card_Q, Card_K, CARD_TYPES

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
            for num in range(13):
                if num == 0 and type == "hearts":
                    card = Card_A_Heart(type, num, 0)
                elif num == 0 and type == "spades":
                    card = Card_A_Spades(type, num, 0)
                elif num == 3:
                    card = Card_4(type, num, 4)
                elif num == 10:
                    card = Card_J(type, num, 0)
                elif num == 11:
                    card = Card_Q(type, num, 0)
                elif num == 12:
                    card = Card_K(type, num, 0)
                else:
                    card = Card(type, num, num +1)
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

    def deal(self, player):
        player.add_card(self.get_lastcard())
        self.remove_card()

    def reset(self):
        pass

    def reset_in_match(self, play_cards):
        self.cards.extend(play_cards)
        self.shuffle()

    def empty(self):
        if len(self.cards) == 0:
            return True
        else: return False

    def get_lastcard(self):
        return self.cards[-1]