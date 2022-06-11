from deck import Deck
from player import Player

class Game:
    def __init__(self, id):
        self.id = id
        self.players = []
        self.deck = Deck()
        self.ready = False
        self.play_card = None
        self.play_cards = []
        self.cur_player = None
        self.sum = 0
        self.winner = None

    def play(self):
        if self.ready == True:
            self.deck.shuffle()

            # Each player have 2 cards
            for player in self.players:
                for _ in range(2):
                    self.deck.deal(player)

    def add_play_card(self, card):
        self.play_card = card
        self.play_cards.append(card)
        self.cur_player.play_card = card
        self.cur_player.check_play_card(self.sum, self)
        self.sum += card.point
        card.effect(self)  

    def get_play_card(self):
        return self.play_card

    def increase_Q(self):
        self.sum += 30

    def decrease_Q(self):
        self.sum -= 30
        if self.sum < 0:
            self.sum = 0

    def kill_K(self, id):
        player = self.find_player(id)
        if player != None:
            self.cur_player.turn = False
            player.turn = True
            player.killed = True
            kill = True
            for card in player.cards:
                if card.get_power() == "4" or card.get_power() == "K":
                    kill = False
                self.play_cards.append(card)

            if kill:
                player.die()
                self.end_turn(player)

    def add_player(self, id):
        if id == 0:
            player = Player(id)
            self.players.append(player)
        else:
            player = Player(id)

            # connect to parent
            parent = self.find_player(id -1)
            if parent != None:
                parent.child = player
                player.parent = parent

            # connect to child
            child = self.find_player(id +1)
            if child != None:
                child.parent = player
                player.child = child
            self.players.append(player)

        # Kick buttons
        for p in self.players:
            p.init_kick_buttons()

    def delete_player(self, id):
        player = self.find_player(id)
        if player == None:
            return
        parent = player.parent
        child = player.child
        if child != None and parent != None:
            child.parent = player.parent
            parent.child = player.child
        elif player.child != None and player.parent == None:
            child.parent = None
        elif player.child == None and player.parent != None:
            parent.child = None

        self.players.remove(player)

    def find_player(self, id):
        for player in self.players:
            if player.id == id:
                return player
        return None

    def end_turn(self, cur_node):
        if cur_node == None:
            return

        cur_node.turn = False
        next_turn_id = -1
        if cur_node.child == None :
            # Find the most parent and change that next turn if there is not next player
            temp_player = cur_node
            while temp_player.parent != None:
                temp_player = temp_player.parent
            next_turn_id = temp_player.id
        else:
            next_turn_id = cur_node.child.id
    
        # Change the player turn
        if next_turn_id != -1:
            player = self.find_player(next_turn_id)
            if not player.killed and len(player.cards) != 0:
                player.turn = True
            else:
                self.end_turn(player)
                        
    def end_game(self):
        count = 0
        temp_player = None
        for player in self.players:
            if len(player.cards) == 0:
                count += 1
            else:
                temp_player = player
        if count == len(self.players) - 1:
            self.winner = temp_player
            return True
        return False

    def reset(self):
        self.deck = Deck()
        self.ready = False
        self.play_card = None
        self.play_cards = []
        self.sum = 0
        self.winner = None

        for player in self.players:
            player.reset()