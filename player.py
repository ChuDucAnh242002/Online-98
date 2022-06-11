"""
    Each player is a node with parent and child
"""


import pygame

from card import CARD_WIDTH, CARD_HEIGHT
from button import Button

FONT = pygame.font.SysFont('comicsans', 24)

BLACK = (0, 0, 0)
RED = (255, 0,0)

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
        self.rect1 = pygame.Rect(390, 550, CARD_WIDTH, CARD_HEIGHT)
        self.rect2 = pygame.Rect(500, 550, CARD_WIDTH, CARD_HEIGHT)
        self.start_button = self.init_start_button()
        self.kick_buttons = []
        self.increase_button = None
        self.decrease_button = None
        self.kill_buttons = []
        self.killed = False
        self.play_card = None
        self.locked = False
        self.turn = False

    def init_start_button(self):
        start_button = None
        if self.id == 0:
            start_button = Button(BUTTON_POS[0], BUTTON_POS[1], "Start game", 0)
        return start_button

    def init_kick_buttons(self):
        if self.id == 0:
            self.init_k_child(self.child, self.id, True)
            self.init_k_parent(self.parent, self.id, True)

    def draw(self, win, x, y, cur = False):
        text = f"Player {self.id}"
        self.text = FONT.render(text, 1, BLACK)
        win.blit(self.text, (x, y))
        back = True
        if cur:
            back = False
        for num, card in enumerate(self.cards):
            card.draw(win, x + 90 + 110*num, y, back)
        if self.turn:
            turn_text = "Waiting"
            turn_text = FONT.render(turn_text, 1, RED)
            win.blit(turn_text, (x, y +25))
        if self.killed :
            killed_text = "Kill"
            killed_text = FONT.render(killed_text, 1, RED)
            win.blit(killed_text, (x, y+ 50))

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

    def get_start_button(self):
        return self.start_button

    def get_kick_buttons(self):
        return self.kick_buttons

    def get_increase_button(self):
        return self.increase_button

    def get_decrease_button(self):
        return self.decrease_button

    def get_kill_buttons(self):
        return self.kill_buttons

    def check_play_card(self, sum, game):
        if self.play_card.power == "Q":
            if sum + 30 <= 98:
                self.increase_button = Button(BUTTON_POS_2[0], BUTTON_POS_2[1], "+30", 1)
            self.decrease_button = Button(BUTTON_POS_3[0], BUTTON_POS_3[1], "-30", 1)

        if self.play_card.power == "K":
            self.init_k_child(self.child, self.id)
            self.init_k_parent(self.parent, self.id)

    def init_k_child(self, child_node, p, kick = False):
        if child_node == None:
            return

        self.init_k(child_node, kick)
        
        self.init_k_child(child_node.child, p, kick)

    def init_k_parent(self, parent_node, p, kick = False):
        if parent_node == None:
            return

        self.init_k(parent_node, kick)

        self.init_k_parent(parent_node.parent, p, kick)

    def init_k(self, cur_node, kick):
        if kick:
            kick_button = self.create_button(cur_node)
            self.kick_buttons.append((cur_node.id, kick_button))

        if len(cur_node.cards) != 0:
            kill_button = self.create_button(cur_node)
            self.kill_buttons.append((cur_node.id, kill_button))

    def create_button(self, cur_node):
        pos = cur_node.id - self.id
        if pos == 1 or pos == -5:
                button = Button(BUTTON_POS_K_1[0], BUTTON_POS_K_1[1], "", 2)
                return button
        elif pos == 2 or pos == -4:
                button = Button(BUTTON_POS_K_2[0], BUTTON_POS_K_2[1], "", 2)
                return button
        elif pos == 3 or pos == -3:
                button = Button(BUTTON_POS_K_3[0], BUTTON_POS_K_3[1], "", 2)
                return button
        elif pos == 4 or pos == -2:
                button = Button(BUTTON_POS_K_4[0], BUTTON_POS_K_4[1], "", 2)
                return button
        elif pos == 5 or pos == -1:
                button = Button(BUTTON_POS_K_5[0], BUTTON_POS_K_5[1], "", 2)
                return button

    def del_button_start(self):
        self.start_button = None

    def del_kick_buttons(self):
        self.kick_buttons = []

    def del_button_Q(self):
        self.increase_button = None
        self.decrease_button = None

    def del_button_K(self):
        self.kill_buttons = []

    def check_die(self, sum):
        if self.cards != []:
            for card in self.cards:
                if sum + card.point <= 98 :
                    return False
                if self.kill_buttons != [] or self.increase_button != None or self.decrease_button != None:
                    return False
            return True
        return False
    
    def die(self):
        self.cards = []
        self.locked = True

    def reset(self):
        self.cards = []
        self.start_button = self.init_start_button()
        self.increase_button = None
        self.decrease_button = None
        self.kill_buttons = []
        self.killed = False
        self.play_card = None
        self.locked = False
        self.turn = False
        
