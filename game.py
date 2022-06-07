import pygame

class Game:
    def __init__(self, id, players, deck):
        self.id = id
        self.players = players
        self.deck = deck
        self.ready = False

    def play(self):
        if self.ready == True:
            self.deck.shuffle()

            # Each player have 2 cards
            for player in self.players:
                for _ in range(2):
                    last_card = self.deck.cards[-1]
                    player.cards.append(last_card)
                    self.deck.cards.pop()

    def cal_result(self):
        pass

    def end_game(self):
        pass