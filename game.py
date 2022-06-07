import pygame

class Game:
    def __init__(self, id, players, deck):
        self.id = id
        self.players = players
        self.deck = deck
        self.ready = False
        self.play_card = None

    def play(self):
        if self.ready == True:
            self.deck.shuffle()

            # Each player have 2 cards
            for player in self.players:
                for _ in range(2):
                    last_card = self.deck.get_lastcard()
                    player.add_card(last_card)
                    self.deck.remove_card()

    def get_play_card(self):
        return self.play_card

    def cal_result(self):
        pass

    def end_game(self):
        pass