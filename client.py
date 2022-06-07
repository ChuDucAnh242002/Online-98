""" 
    author: Chu Duc Anh
    Github: https://github.com/ChuDucAnh242002
    A game of calculate to 98 created High School Le Hong Phong in Viet Nam
"""

import pygame
import sys
import os

from button import BLUE, Button
from game import Game
from network import Network
from player import Player
from deck import Deck

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1200, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("98")

CLOCK = pygame.time.Clock()
FPS = 60

# Font
SUM_FONT = pygame.font.SysFont('comicsans', 36)

# Image
bg = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'Background', 'background.jpg')), (WIDTH, HEIGHT))

# Size and pos
BUTTON_POS = (375, 312)
BUTTON_POS_2 = (100, 600)
BUTTON_POS_3 = (180, 600)

# CARD_POS = (500, 200)
PLAYER_POS_0_X, PLAYER_POS_0_Y = 300, 550
PLAYER_POS_1_X, PLAYER_POS_1_Y = 0, 300
PLAYER_POS_2_X, PLAYER_POS_2_Y = 300, 10
PLAYER_POS_3_X, PLAYER_POS_3_Y = 750, 10
PLAYER_POS_4_X, PLAYER_POS_4_Y = 850, 300
PLAYER_POS_5_X, PLAYER_POS_5_Y = 750, 550


def draw_bg():
    WIN.blit(bg, (0, 0))  

def draw_players(cur_player):
    cur_player.draw(WIN, PLAYER_POS_0_X, PLAYER_POS_0_Y, True)
    draw_child(cur_player.child, cur_player.id)
    draw_parent(cur_player.parent, cur_player.id)

def draw_pos(cur_player, p):
    pos = cur_player.id - p
    if pos == 1 or pos == -5:
        cur_player.draw(WIN, PLAYER_POS_1_X, PLAYER_POS_1_Y)
    elif pos == 2 or pos == -4:
        cur_player.draw(WIN, PLAYER_POS_2_X, PLAYER_POS_2_Y)
    elif pos == 3 or pos == -3:
        cur_player.draw(WIN, PLAYER_POS_3_X, PLAYER_POS_3_Y)
    elif pos == 4 or pos == -2:
        cur_player.draw(WIN, PLAYER_POS_4_X, PLAYER_POS_4_Y)
    elif pos == 5 or pos == -1:
        cur_player.draw(WIN, PLAYER_POS_5_X, PLAYER_POS_5_Y)

def draw_child(cur_player, p):
    if cur_player == None:
        return
    draw_pos(cur_player, p)
    draw_child(cur_player.child, p)

def draw_parent(cur_player, p):
    if cur_player == None:
        return
    draw_pos(cur_player, p)
    draw_parent(cur_player.parent, p)

def draw_sum(game):
    sum_text = "Sum: " + str(game.sum)
    sum_text = SUM_FONT.render(sum_text, 1, BLUE)
    WIN.blit(sum_text, (0, 0))

def draw_win(game, players, deck, cur_player, increase_button, decrease_button):
    global n, start_button, kill_buttons
    draw_bg()
    draw_players(cur_player)
    
    if game.ready == False and cur_player.id == 0:
        start_button = Button(BUTTON_POS[0], BUTTON_POS[1], "Start game", 0)
        start_button.draw(WIN)

    elif game.ready == True:
        deck.draw(WIN)
        draw_sum(game)
        play_card = game.get_play_card()
        if play_card == None:
            return
        play_card.draw_play(WIN)
        if play_card.power == "Q" :
            # if game.sum + 30 <= 98:
            #     increase_button = cur_player.get_increase_button()
            # decrease_button = cur_player.get_decrease_button()
            if increase_button != None:
                increase_button.draw(WIN, middle = False)
            if decrease_button != None:
                decrease_button.draw(WIN, middle = False)
            
    #     if play_card.power == "K":
    #         kill_buttons = cur_player.get_kill_buttons()
    #         for kill_button in kill_buttons:
    #             kill_button[1].draw(WIN, middle = False)
    #         cur_player.locked = True

def handle_click(cur_player, pos):
    global n
    if cur_player.click1(pos):
        n.send("click1")
        return 

    elif cur_player.click2(pos):
        n.send("click2")
        return 

def main():
    global n, start_button, increase_button, decrease_button, kill_buttons
    p = int(n.getP())

    start_button = None
    increase_button = None
    decrease_button = None
    kill_buttons = []

    run = True

    while run:
        CLOCK.tick(FPS)

        try: 
            game = n.send("get")
            players = game.players
            cur_player = game.cur_player
            deck = game.deck

        except:
            run = False
            print("Couldn't get game")
            break
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button != None:
                    if start_button.click(pos):
                        n.send("start")
                        start_button = None

                if not cur_player.die(game.sum):
                    if game.sum + 30 <= 98:
                        if increase_button != None:
                            if increase_button.click(pos):
                                n.send("increase")
                                increase_button = None
                                decrease_button = None
                                # cur_player.del_button_Q()
                                # game.play_card.power = None
                                # cur_player.locked = False
                    
                    if decrease_button != None:
                        if decrease_button.click(pos):
                            n.send("decrease")
            #                 game.decrease_Q()
            #                 cur_player.del_button_Q()
                            increase_button = None
                            decrease_button = None
            #                 game.play_card.power = None
            #                 cur_player.locked = False

            #         if kill_buttons != []:
            #             for kill_button in kill_buttons:
            #                 if kill_button[1].click(pos):
            #                     game.kill_K(kill_button[0])
            #                     game.play_card.power = None
            #                     cur_player.locked = False
            #                     kill_buttons = []
            #                     cur_player.del_button_K()
                        
                    if not cur_player.locked:
                        handle_click(cur_player, pos)

        if deck.empty():
            n.send("reset in match")
            # deck.reset_in_match(game.play_cards)
            # game.play_cards = []

        play_card = game.get_play_card()
        if play_card != None:
            if play_card.power == "Q":
                if game.sum + 30 <= 98:
                    increase_button = cur_player.get_increase_button()
                decrease_button = cur_player.get_decrease_button()
                n.send("locked")

        draw_win(game, players, deck, cur_player, increase_button, decrease_button)

        pygame.display.update()

def menu():
    global n

    run = True
    menu_button = Button(BUTTON_POS[0], BUTTON_POS[1], "Click to join the server", 0)

    while run:
        CLOCK.tick(FPS)
        draw_bg()
        menu_button.draw(WIN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu_button.click(pos):
                    try:
                        run = False
                        n = Network()
                        main()
                        
                    except:
                        print("Server Offline")
                        quit()

        

def quit():
    pygame.quit()
    sys.exit()
        
if __name__ == "__main__":
    while True:
        menu()