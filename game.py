from deck import Deck

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
        self.cur_player.check_play_card(self.sum)
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
        player = self.players[id]
        self.cur_player.turn = False
        player.turn = True
        player.killed = True
        kill = True
        for card in player.cards:
            if card.get_power() == "4":
                kill = False
            self.play_cards.append(card)

        if kill:
            player.die()
            self.end_turn(player)

    def delete_player(self, id):
        for p in self.players:
            if p.id == id:
                player = p
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

    def end_turn(self, cur_node):
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
            for player in self.players:
                if player.id == next_turn_id :
                    if not player.killed:
                        player.turn = True
                    else:
                        self.end_turn(player)
                        
    def cal_result(self):
        pass

    def end_game(self):
        pass

    def reset(self):
        self.ready = True
        self.play_card = None
        self.play_cards = []
        self.sum = 0

        for player in self.players:
            player.reset()
        
        self.deck.shuffle()

        for player in self.players:
            for _ in range(2):
                self.deck.deal(player)