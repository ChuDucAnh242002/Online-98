class Game:
    def __init__(self, id, players, deck):
        self.id = id
        self.players = players
        self.deck = deck
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
        self.sum += (card.point)
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

    def cal_result(self):
        pass

    def end_game(self):
        pass

    def reset(self):
        self.ready = False
        self.play_card = None
        self.play_cards = []
        self.sum = 0