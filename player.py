"""
    Each player is a node with parent and child
"""


import pygame

from card import Card, CARD_WIDTH, CARD_HEIGHT

FONT = pygame.font.SysFont('comicsans', 24)

BLACK = (0, 0, 0)

class Node:
    def __init__(self, id):
        self.id = id
        self.parent = None
        self.child = None

class Player(Node):
    def __init__(self, id):
        super().__init__(id)
        self.cards = []
        self.rect1 = None
        self.rect2 = None

    def draw(self, win, x, y, cur = False):
        text = f"Player {self.id}"
        self.text = FONT.render(text, 1, BLACK)
        win.blit(self.text, (x, y))
        back = True
        if cur:
            back = False
        for num, card in enumerate(self.cards):
            if num == 0:
                self.rect1 = pygame.Rect(x + 100 + 100*num, y, CARD_WIDTH, CARD_HEIGHT)
                card.draw(win, self.rect1.x, self.rect1.y, back)
            else:
                self.rect2 = pygame.Rect(x + 100 + 100*num, y, CARD_WIDTH, CARD_HEIGHT)
                card.draw(win, self.rect2.x, self.rect2.y, back)

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def play_card(self):
        pass

    def click1(self, pos):
        if self.rect1.collidepoint(pos):
            return True
        return False

    def click2(self, pos):
        if self.rect2.collidepoint(pos):
            return True
        return False

    def get_card(self, num):
        return self.cards[num]

    def die(self):
        pass
        