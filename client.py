""" 
    author: Chu Duc Anh
    Github: https://github.com/ChuDucAnh242002
    A game of calculate to 98 created High School Le Hong Phong in Viet Nam
"""

import pygame
import sys
import os

from button import BLUE, Button
from network import Network
from game import Game_Poker

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1200, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("98")

CLOCK = pygame.time.Clock()
FPS = 60

# Font
SUM_FONT = pygame.font.SysFont('comicsans', 36)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Image
bg = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'Background', 'background.jpg')), (WIDTH, HEIGHT))

# Size and pos
BUTTON_POS = (375, 250)
BUTTON_POS_1 = (375, 360)
PLAYER_POS = [(300, 550), (0, 300), (300, 10), (750, 10), (850, 300), (750, 550)]


def draw_bg():
    WIN.blit(bg, (0, 0))  

def draw_players(cur_player):
    cur_player.draw(WIN, PLAYER_POS[0][0], PLAYER_POS[0][1], True)
    draw_child(cur_player.child, cur_player.id)
    draw_parent(cur_player.parent, cur_player.id)

def draw_pos(cur_player, p):
    pos = cur_player.id - p
    cur_player.draw(WIN, PLAYER_POS[pos][0], PLAYER_POS[pos][1])

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

def draw_win(game, deck, cur_player):
    draw_bg()
    draw_players(cur_player)
    start_button = cur_player.get_start_button()
    if start_button != None:
        start_button.draw(WIN)

    kick_buttons = cur_player.get_kick_buttons()
    if kick_buttons != []:
        for kick_button in kick_buttons:
            kick_button[1].draw(WIN, middle = False)
            
def draw_win_98(game, deck, cur_player):
    draw_win(game, deck, cur_player)

    if game.ready == True:
        deck.draw(WIN)
        draw_sum(game)
        play_card = game.get_play_card()
        if play_card == None:
            return
        play_card.draw_play(WIN)
        if play_card.get_power() == "Q" :
            increase_button = cur_player.get_increase_button()
            decrease_button = cur_player.get_decrease_button()
            if increase_button != None:
                increase_button.draw(WIN, middle = False)
            if decrease_button != None:
                decrease_button.draw(WIN, middle = False)
            
        if play_card.get_power() == "K":
            kill_buttons = cur_player.get_kill_buttons()
            for kill_button in kill_buttons:
                kill_button[1].draw(WIN, middle = False)

def draw_win_poker(game, deck, cur_player):
    draw_win(game, deck, cur_player)

def handle_click(cur_player, pos):
    global n, game
    
    if cur_player.click1(pos):
        n.send("click1")
        game = n.send("get")
        if game.play_card != None:
            power = game.play_card.get_power()
            if power != "Q" and power != "K":
                n.send("end turn")

    elif cur_player.click2(pos):
        n.send("click2")
        game = n.send("get")
        if game.play_card != None:
            power = game.play_card.get_power()
            if power != "Q" and power != "K":
                n.send("end turn")

def handle_click_poker(cur_player, pos):
    if cur_player.click(pos):
        rect_num = cur_player.get_rect_num()
        cur_player.remove_chip(rect_num)
        
def draw_winner(winner):
    winner_text = "Survivor: " + str(winner.id)
    winner_text = WINNER_FONT.render(winner_text, 1, BLUE)
    WIN.blit(winner_text, (WIDTH //2 - winner_text.get_width() /2, HEIGHT //2 - winner_text.get_height() /2))

def draw_offline():
    draw_bg()
    offline_text = "Server Offline"
    offline_text = SUM_FONT.render(offline_text, 1, BLUE)
    WIN.blit(offline_text, (WIDTH //2 - offline_text.get_width() /2,HEIGHT //2 - offline_text.get_height() /2))
    pygame.display.update()
    pygame.time.delay(3000)

def main_98():
    global n
    p = int(n.getP())

    run = True

    while run:
        CLOCK.tick(FPS)

        try: 
            game = n.send("get")
            cur_player = game.cur_player
            deck = game.deck

        except:
            run = False
            print("Couldn't get game")
            break
        
        start_button = cur_player.get_start_button()
        kick_buttons = cur_player.get_kick_buttons()
        increase_button = cur_player.get_increase_button()
        decrease_button = cur_player.get_decrease_button()
        kill_buttons = cur_player.get_kill_buttons()

        if increase_button != None or decrease_button != None:
            n.send("locked")

        if kill_buttons != []:
            n.send("locked")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button != None:
                    if start_button.click(pos):
                        n.send("start")

                if kick_buttons != []:
                    for kick_button in kick_buttons:
                        if kick_button[1].click(pos):
                            datas = ["kick", str(kick_button[0])]
                            data = " ".join(datas)
                            n.send(data)

                if cur_player.check_die(game.sum):
                    n.send("die")

                if not cur_player.check_die(game.sum) and (increase_button != None or decrease_button != None or kill_buttons != None) :
                    if not cur_player.locked and cur_player.turn:
                        handle_click(cur_player, pos)

                    if increase_button != None:
                        if increase_button.click(pos):
                            n.send("increase")
                            n.send("end turn")
                    
                    if decrease_button != None:
                        if decrease_button.click(pos):
                            n.send("decrease")
                            n.send("end turn")

                    if kill_buttons != []:
                        for kill_button in kill_buttons:
                            if kill_button[1].click(pos):
                                datas = ["kill", str(kill_button[0])]
                                data = " ".join(datas)
                                n.send(data)
                    
        if deck.empty():
            n.send("reset in match")

        if game.end_game() and len(game.players) > 1:
            draw_win_98(game, deck, cur_player)
            draw_winner(game.winner)
            pygame.display.update()
            pygame.time.delay(5000)
            n.send("reset")

        draw_win_98(game, deck, cur_player)

        pygame.display.update()

def main_poker():
    # global n
    game = Game_Poker(10)
    for num in range(6):
        game.add_player(num)

    p = 0
    deck = game.deck
    cur_player = game.find_player(p)
    player_5 = game.find_player(5)
    game.cur_player = cur_player
    game.init_chips(cur_player)

    run = True

    while run:
        
        CLOCK.tick(FPS)

        start_button = cur_player.get_start_button()
        kick_buttons = cur_player.get_kick_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button != None:
                    if start_button.click(pos):
                        game.ready = True
                        game.play()
                        cur_player.turn = True
                        cur_player.big_blind = True
                        player_5.small_blind = True
                        cur_player.del_button_start()
                        cur_player.del_kick_buttons()

                if kick_buttons != []:
                    for kick_button in kick_buttons:
                        if kick_button[1].click(pos):
                            id = int(kick_button[0])
                            game.delete_player(id)
                            cur_player.del_kick_buttons_id(id)
                handle_click_poker(cur_player, pos)

        draw_win_poker(game, deck, cur_player)

        pygame.display.update()

def menu():
    global n

    run = True
    menu_button = Button(BUTTON_POS[0], BUTTON_POS[1], "98", 0)
    # poker_button = Button(BUTTON_POS_1[0], BUTTON_POS_1[1], "Poker", 0)

    while run:
        CLOCK.tick(FPS)
        draw_bg()
        menu_button.draw(WIN, middle= False)
        # poker_button.draw(WIN, middle= False)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu_button.click(pos):
                    run = False
                    n = Network()
                    connect(main_98())

                # if poker_button.click(pos):
                #     run = False
                    # n = Network()
                    # connect(main_poker())

def connect(main):
    # global n 

    try:
        # n = Network()
        try:
            main()
        except:
            quit()
    except:
        try:
            draw_offline()
        except:
            quit()
    
def quit():
    pygame.quit()
    sys.exit()
        
if __name__ == "__main__":
    run = True
    while run:
        try:
            menu()
        except ValueError as e:
            print(e)
            run = False
            print("You have been kicked")
            quit()