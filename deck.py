import random
import pygame

from card import Card, Card_4, Card_A_Heart, Card_A_Spades, Card_J, Card_Q, Card_K, CARD_TYPES, CARD_BACK

# Size
DECK_WIDTH, DECK_HEIGHT = 210, 285
DECK_POS_X, DECK_POS_Y = 400, 200

class Deck:
    def __init__(self):
        self.cards = self.init_cards()
        self.x = DECK_POS_X
        self.y = DECK_POS_Y

    def init_cards(self):
        cards = []
        for type in CARD_TYPES:
            for num in range(13):
                if num == 0 and type == "Hearts":
                    card = Card_A_Heart(type, num, 0, "A_H")
                elif num == 0 and type == "Spades":
                    card = Card_A_Spades(type, num, 0, "A_S")
                elif num == 3:
                    card = Card_4(type, num, 4, "4")
                elif num == 10:
                    card = Card_J(type, num, 0, "J")
                elif num == 11:
                    card = Card_Q(type, num, 0, "Q")
                elif num == 12:
                    card = Card_K(type, num, 0, "K")
                else:
                    card = Card(type, num, num +1)
                cards.append(card)
        return cards

    def draw(self, win):
        image = pygame.transform.scale(CARD_BACK, (DECK_WIDTH, DECK_HEIGHT))
        win.blit(image, (self.x, self.y))

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