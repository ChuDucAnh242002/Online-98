import socket
from _thread import *
import pickle
import pygame

from player import Player
from game import Game

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.0.245"
port = 5555

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection")

connections = 0
idCount = 0
games = {}

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try: 
            data = conn.recv(8192*3).decode()

            if gameId in games:
                game = games[gameId]

                players = game.players
                cur_player = players[p]
                for player in players:
                    if player.id == p:
                        cur_player = player
                        break
                
                deck = game.deck
                game.cur_player = cur_player
                if not data:
                    print("No data")
                    break

                else:
                    datas = data.split(" ")
                    if data == "reset":
                        game.reset()

                    if data == "start":
                        game.ready = True
                        game.play()
                        cur_player.turn = True

                    if data == "click1":
                        card = cur_player.get_card(0)
                        game.add_play_card(card)
                        cur_player.remove_card(card)
                        deck.deal(cur_player)

                    if data == "click2":
                        card = cur_player.get_card(1)
                        game.add_play_card(card)
                        cur_player.remove_card(card)
                        deck.deal(cur_player)

                    if data == "reset in match":
                        deck.reset_in_match(game.play_cards)
                        game.play_cards = []

                    if data == "locked":
                        cur_player.locked = True

                    if data == "increase":
                        game.increase_Q()
                        game.play_card.power = None
                        cur_player.locked = False
                        cur_player.del_button_Q()

                    if data == "decrease":
                        game.decrease_Q()
                        game.play_card.power = None
                        cur_player.locked = False
                        cur_player.del_button_Q()

                    if datas[0] == "kill":
                        id = datas[1]
                        game.kill_K(int(id))
                        game.play_card.power = None
                        cur_player.locked = False
                        cur_player.del_button_K()

                    if data == "end turn":
                        game.end_turn(cur_player)
                        if cur_player.killed:
                            if game.play_card.point == 4:
                                cur_player.killed = False
                            else:
                                cur_player.die()
                        if game.sum > 98:
                            cur_player.die()
                            game.sum = game.sum - game.play_card.point

                    if data == "die":
                        cur_player.die()
                        
                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                print("No game")
        except socket.error as e:
            print(e)
            break
    print("Lost connection")
    try:
        if p == 0:
            del games[gameId]
            print("Closing game", gameId)
    except:
        pass
    
    idCount -= 1
    game.delete_player(p)
    conn.close()

def main():
    global connections, idCount
    while True:
        if connections < 6:
            connections += 1
            conn, addr = s.accept()
            print("Connected to: ", addr)

            idCount += 1
            p = (idCount - 1) %6
            gameId = (p) //6

            if idCount %6 == 1:
                games[gameId] = Game(gameId)
                player = Player(p)
                games[gameId].players.append(player)
                print("Creating a new game...")

            else:
                player = Player(p)
                parent = games[gameId].players[p -1]
                parent.child = player
                player.parent = parent
                games[gameId].players.append(player)

            start_new_thread(threaded_client, (conn, p, gameId))
            
            
if __name__ == "__main__":
    main()

