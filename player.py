"""
    Each player is a node with parent and child
"""


import pygame

from card import CARD_WIDTH, CARD_HEIGHT
from button import Button

FONT = pygame.font.SysFont('comicsans', 24)

BLACK = (0, 0, 0)

# Size and pos
BUTTON_POS = (375, 312)
BUTTON_POS_2 = (100, 600)
BUTTON_POS_3 = (180, 600)
BUTTON_POS_K_1 = (0, 350) 
BUTTON_POS_K_2 = (300, 60)
BUTTON_POS_K_3 = (750, 60)
BUTTON_POS_K_4 = (850, 350)
BUTTON_POS_K_5 = (750, 600)

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
        self.increase_button = None
        self.decrease_button = None
        self.kill_buttons = []
        self.play_card = None

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

    def get_increase_button(self):
        return self.increase_button

    def get_decrease_button(self):
        return self.decrease_button

    def get_kill_buttons(self):
        return self.kill_buttons

    def check_play_card(self):
        if self.play_card.power == "Q":
            self.increase_button = Button(BUTTON_POS_2[0], BUTTON_POS_2[1], "+30", 1)
            self.decrease_button = Button(BUTTON_POS_3[0], BUTTON_POS_3[1], "-30", 1)

        if self.play_card.power == "K":
            self.init_k_child(self.child, self.id)

    def init_k_child(self, child_node, p):
        if child_node == None:
            return

        self.init_k(child_node)
        
        self.init_k_child(child_node.child, p)

    def init_k_parent(self, parent_node, p):
        if parent_node == None:
            return

        self.init_k(parent_node)

        self.init_k_parent(parent_node.parent, p)

    def init_k(self, cur_node):
        pos = cur_node.id - self.id
        if pos == 1 or pos == -5:
            kill_button = Button(BUTTON_POS_K_1[0], BUTTON_POS_K_1[1], "", 2)
            self.kill_buttons.append((cur_node.id, kill_button))
        elif pos == 2 or pos == -4:
            kill_button = Button(BUTTON_POS_K_2[0], BUTTON_POS_K_2[1], "", 2)
            self.kill_buttons.append((cur_node.id, kill_button))
        elif pos == 3 or pos == -3:
            kill_button = Button(BUTTON_POS_K_3[0], BUTTON_POS_K_3[1], "", 2)
            self.kill_buttons.append((cur_node.id, kill_button))
        elif pos == 4 or pos == -2:
            kill_button = Button(BUTTON_POS_K_4[0], BUTTON_POS_K_4[1], "", 2)
            self.kill_buttons.append((cur_node.id, kill_button))
        elif pos == 5 or pos == -1:
            kill_button = Button(BUTTON_POS_K_5[0], BUTTON_POS_K_5[1], "", 2)
            self.kill_buttons.append((cur_node.id, kill_button))

    def del_button_Q(self):
        self.increase_button = None
        self.decrease_button = None

    def del_button_K(self):
        self.kill_buttons = []

    def die(self):
        pass
        