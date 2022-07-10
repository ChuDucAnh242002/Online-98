"""
    Each player is a node with parent and child
"""


import pygame

from card import CARD_WIDTH, CARD_HEIGHT
from button import Button
from chip import Stack

# Font
AMOUNT_FONT = pygame.font.SysFont("comicsans", 36)
FONT = pygame.font.SysFont('comicsans', 24)

BLACK = (0, 0, 0)
RED = (255, 0,0)

# Size and pos
BUTTON_POS = (375, 312)
BUTTON_POS_2 = (100, 600)
BUTTON_POS_3 = (180, 600)
BUTTON_POS_K = [(300, 600), (0, 350), (300, 60), (750, 60), (850, 350), (750, 600)]
CHIP_POS = {
    0: (10, 500),
    1: (135, 500),
    2: (10, 625),
    3: (135, 625)
}

class Node:
    def __init__(self, id):
        self.id = id
        self.parent = None
        self.child = None

class Player(Node):
    def __init__(self, id):
        super().__init__(id)
        self.cards = []
        self.locked = False
        self.turn = False
        self.start_button = self.init_start_button()
        self.kick_buttons = []

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
        # Player cards
        for num, card in enumerate(self.cards):
            card.draw(win, x + 100 + 110*num, y, back)

        # Player turn
        if self.turn:
            turn_text = "Waiting"
            turn_text = FONT.render(turn_text, 1, RED)
            win.blit(turn_text, (x, y +25))

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def get_card(self, num):
        return self.cards[num]

    def get_start_button(self):
        return self.start_button

    def get_kick_buttons(self):
        return self.kick_buttons

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
        button = Button(BUTTON_POS_K[int(pos)][0], BUTTON_POS_K[int(pos)][1], "", 2)
        return button
   
    def del_button_start(self):
        self.start_button = None

    def del_kick_buttons(self):
        self.kick_buttons = []

    def del_kick_buttons_id(self, id):
        for kick_button in self.kick_buttons:
            if int(kick_button[0]) == id:
                self.kick_buttons.remove(kick_button)

    def reset(self):
        self.cards = []
        self.start_button = self.init_start_button()
        self.locked = False
        self.turn = False

class Player_98(Player):
    def __init__(self, id):
        super().__init__(id)
        self.rect1 = pygame.Rect(390, 550, CARD_WIDTH, CARD_HEIGHT)
        self.rect2 = pygame.Rect(500, 550, CARD_WIDTH, CARD_HEIGHT)
        self.increase_button = None
        self.decrease_button = None
        self.kill_buttons = []
        self.killed = False
        self.play_card = None

    def draw(self, win, x, y, cur = False):
        super().draw(win, x, y, cur)

        # Player get killed
        if self.killed :
            killed_text = "Kill"
            killed_text = FONT.render(killed_text, 1, RED)
            win.blit(killed_text, (x, y+ 50))

    def click1(self, pos):
        if self.rect1.collidepoint(pos):
            return True
        return False

    def click2(self, pos):
        if self.rect2.collidepoint(pos):
            return True
        return False

    def get_increase_button(self):
        return self.increase_button

    def get_decrease_button(self):
        return self.decrease_button

    def get_kill_buttons(self):
        return self.kill_buttons

    def check_play_card(self, sum):
        if self.play_card.power == "Q":
            if sum + 30 <= 98:
                self.increase_button = Button(BUTTON_POS_2[0], BUTTON_POS_2[1], "+30", 1)
            self.decrease_button = Button(BUTTON_POS_3[0], BUTTON_POS_3[1], "-30", 1)

        if self.play_card.power == "K":
            self.init_k_child(self.child, self.id)
            self.init_k_parent(self.parent, self.id)

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
        super().reset()
        self.increase_button = None
        self.decrease_button = None
        self.kill_buttons = []
        self.killed = False
        self.play_card = None
        
class Player_Poker(Player):
    def __init__(self, id):
        super().__init__(id)
        self.big_blind = False
        self.small_blind = False
        self.stack = Stack(2, "1:2")
        self.chips = self.stack.chips
        self.chips_color = []
        self.chips_amount = []
        self.init_chips()
        self.rects = self.init_rects()
        self.rect = None
        self.rect_num = None

    def init_rects(self):
        rects = []
        for index in range(4):
            rect = pygame.Rect(CHIP_POS[index][0], CHIP_POS[index][1], 75, 75)
            rects.append(rect)
        return rects

    def init_chips(self):
        for item in self.chips.items():
            color = item[0]
            value = item[1]
            amount = len(value)
            self.chips_color.append(color)
            self.chips_amount.append(amount)

    def draw(self, win, x, y, cur = False):
        super().draw(win, x, y, cur)

        if self.big_blind or self.small_blind:
            blind_text = ""
            if self.big_blind: blind_text = "Big Blind"
            elif self.small_blind: blind_text = "SM. Blind"
            blind_text = FONT.render(blind_text, 1, RED)
            win.blit(blind_text, (x, y +50))

        if cur:
            index = 0
            for value in self.chips.values():
                if len(value):
                    chip = value[0]
                    chip.draw(win, CHIP_POS[index][0], CHIP_POS[index][1])
                    index += 1

            for index_a, amount in enumerate(self.chips_amount):
                amount = str(amount)
                amount_text = AMOUNT_FONT.render(amount, 1, BLACK)
                win.blit(amount_text, (CHIP_POS[index_a][0] + 38 - amount_text.get_width() /2, CHIP_POS[index_a][1] + 75))

    def click(self, pos):
        for num, rect in enumerate(self.rects):
            if rect.collidepoint(pos):
                self.rect = rect
                self.rect_num = num
                return True
        return False

    def get_rect_num(self): return self.rect_num

    def remove_chip(self, num):
        self.chips_amount[num] -= 1
    