"""
    Each player is a node with parent and child
"""


import pygame

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

    def draw(self, win, x, y):
        text = f"Player {self.id}"
        self.text = FONT.render(text, 1, BLACK)
        win.blit(self.text, (x, y))

    def add_card(self):
        pass

    def remove_card(self):
        pass

    def play_card(self):
        pass

    def die(self):
        pass
        