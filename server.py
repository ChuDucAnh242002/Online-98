import socket
from _thread import *
import pickle

# from player import Player
from game import Game_98, Game_Poker

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "172.104.234.136"
port = 5555

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection")

connections = 0
idCount = 0
player_num = -1
games = {}
MAX_PER_ROOM = 6

def threaded_client(conn, p, gameId):
    global idCount, player_num, games
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try: 
            data = conn.recv(8192*4).decode()

            if gameId in games:
                game = games[gameId]

                cur_player = game.find_player(p)
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
                        cur_player.del_button_start()
                        cur_player.del_kick_buttons()

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
                        cur_player.locked = False
                        cur_player.killed = False
                        game.kill_K(int(id))
                        game.play_card.power = None
                        cur_player.del_button_K()

                    if datas[0] == "kick":
                        id = int(datas[1])
                        game.delete_player(id)
                        cur_player.del_kick_buttons_id(id)

                    if data == "end turn":
                        game.end_turn(cur_player)
                        if cur_player.killed:
                            if game.play_card.get_power() == "4" or game.play_card.get_power() == "K":
                                cur_player.killed = False
                            else:
                                cur_player.die()
                        if game.sum > 98 :
                            cur_player.die()
                            game.sum = game.sum - game.play_card.point

                    if data == "die":
                        cur_player.die()
                        game.end_turn(cur_player)
                        
                    if data == "delete game":
                        del games[gameId]
                        print("Closing game", gameId)
                        break
                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                print("No game")
        except socket.error as e:
            print(e)
            print("socket error 1")
            break
    print("Lost connection")
    try:
        if len(games[gameId].players) <= 1:
            del games[gameId]
            print("Closing game", gameId)
    except:
        pass
    
    idCount -= 1
    player_num -= 1
    try:
        games[gameId].delete_player(p)
    except: pass
    conn.close()

def main():
    global connections, idCount, player_num
    while True:
        if connections < 18:
            connections += 1
            conn, addr = s.accept()
            print("Connected to: ", addr)

            idCount += 1
            player_num += 1
            p = player_num %MAX_PER_ROOM
            gameId = player_num //MAX_PER_ROOM

            if len(games) != 0:
                if games[gameId].ready:
                    player_num = player_num +MAX_PER_ROOM -p
                    idCount = idCount +MAX_PER_ROOM -p
                    p = player_num %MAX_PER_ROOM
                    gameId = player_num //MAX_PER_ROOM

            if idCount %MAX_PER_ROOM == 1:
                games[gameId] = Game_98(gameId)
                games[gameId].add_player(p)
                print("Creating a new game...")

            elif not games[gameId].ready:
                games[gameId].add_player(p)

            try:
                start_new_thread(threaded_client, (conn, p, gameId))
            except socket.error as e:
                print(str(e))
                del games[gameId]

                 
if __name__ == "__main__":
    main()

