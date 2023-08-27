"""
This script defines the classes
    *

The classes do...

Dependencies
    * `multideck` (personal script)
    * `players` (personal script)
"""


from blackjack.multideck import MultiDeck
from blackjack.players import Dealer, Player


class GameControl:
    def __init__(self, num_players=6, min_bet=10, num_decks=6, verbose=True):
        self.verbose = verbose
        self.min_bet = min_bet
        self.deck = None
        self.dealer = None
        self.players = []
        self.round = 0

        self.standard_setup(num_players=num_players, num_decks=num_decks)

    def __str__(self):
        use_s = ["", "s"]
        return f"GameControl consisting of {self.player_count} player{use_s[self.player_count != 1]}"

    @property
    def player_count(self) -> int:
        return len(self.players)

    def standard_setup(self, num_players, num_decks):
        self.add_deck(num_decks=num_decks)
        self.add_dealer()
        [self.add_player() for _ in range(num_players)]
        return self  # inplace=False

    def add_deck(self, num_decks=6, init_empty=False) -> MultiDeck:
        if self.deck is not None:
            raise ValueError("A deck already exists in this game")
        new_deck = MultiDeck(num_decks=num_decks, init_empty=init_empty)
        self.deck = new_deck
        return new_deck

    def add_dealer(self) -> Dealer:
        if self.dealer is not None:
            raise ValueError("A dealer already exists in this game")
        new_dealer = Dealer(game=self)
        self.dealer = new_dealer
        return new_dealer

    def add_player(self, name=None, money=500) -> Player:
        if name in [p.name for p in self.players]:
            raise ValueError(f"The name {name} is already taken")
        new_player = Player(game=self, name=name, money=money)
        self.players.append(new_player)
        return new_player

    def play_round(self):
        self.round += 1

        # place bets the deal
        [player.add_hand() for player in self.players]
        [player[0].deal() for player in self.players]
        self.dealer.deal()

        print(self.dealer)
        for player in self.players:
            print(player)
            for hand in player.hands:
                hand.play_hand()  # TODO: implement this
