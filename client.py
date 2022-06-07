""" 
    author: Chu Duc Anh
    Github: https://github.com/ChuDucAnh242002
    A game of calculate to 98 created High School Le Hong Phong in Viet Nam
"""

import pygame
import sys
import os

from button import Button
from game import Game
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

# Image
bg = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'Background', 'background.jpg')), (WIDTH, HEIGHT))

# Size and pos
DECK_POS_X, DECK_POS_Y = 300, 200
PLAYER_POS_0_X, PLAYER_POS_0_Y = 300, 550
PLAYER_POS_1_X, PLAYER_POS_1_Y = 0, 300
PLAYER_POS_2_X, PLAYER_POS_2_Y = 300, 10
PLAYER_POS_3_X, PLAYER_POS_3_Y = 750, 10
PLAYER_POS_4_X, PLAYER_POS_4_Y = 900, 300
PLAYER_POS_5_X, PLAYER_POS_5_Y = 750, 550



def draw_bg():
    WIN.blit(bg, (0, 0))  

def draw_players(cur_player):
    cur_player.draw(WIN, PLAYER_POS_0_X, PLAYER_POS_0_Y)
    # print(cur_player.parent.id)
    draw_child(cur_player.child, cur_player.id)
    draw_parent(cur_player.parent, cur_player.id)

def draw_pos(cur_player, p):
    pos = p - cur_player.id
    if pos == -1 or pos == 5:
        cur_player.draw(WIN, PLAYER_POS_1_X, PLAYER_POS_1_Y)
    elif pos == -2 or pos == 4:
        cur_player.draw(WIN, PLAYER_POS_2_X, PLAYER_POS_2_Y)
    elif pos == -3 or pos == 3:
        cur_player.draw(WIN, PLAYER_POS_3_X, PLAYER_POS_3_Y)
    elif pos == -4 or pos == 2:
        cur_player.draw(WIN, PLAYER_POS_4_X, PLAYER_POS_4_Y)
    elif pos == -5 or pos == 1:
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


def draw_win(game, players, deck, cur_player):
    draw_bg()
    deck.draw(WIN)
    draw_players(cur_player)

def init_player():
    """
    Create 6 player
    return: list of players
    """
    players = []
    for id in range(6):
        player = Player(id)
        if id == 0:
            players.append(player) 
            continue
        else:
            parent = players[id -1]
            parent.child = player
            player.parent = parent
        players.append(player)
    return players

def main():

    players = init_player()
    p = 0
    cur_player = players[p]
    deck = Deck(DECK_POS_X, DECK_POS_Y)
    game = Game(0, players, deck)


    run = True

    while run:
        CLOCK.tick(FPS)
        draw_win(game, players, deck, cur_player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            

        pygame.display.update()



def lobby():
    run = True

def menu():
    run = True
    menu_button = Button(375, 312, "Click to join the server")

    while run:
        CLOCK.tick(FPS)
        draw_bg()
        menu_button.draw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu_button.click(pos):
                    # try;
                    run = False
                    main()
                    break
                    # except:
                    #     print("Server Offline")

        pygame.display.update()

        
if __name__ == "__main__":
    while True:
        menu()