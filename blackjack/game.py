"""
This script defines the classes
    *

The classes do...

Dependencies
    * `deck` (personal script)
    * `players` (personal script)
"""


from blackjack import deck as deck_
from blackjack import participants


class Game:
    """
    A class to control the Blackjack game.
    """

    deck: deck_.Deck
    dealer: participants.Dealer
    players: list[participants.Player]
    min_bet: int
    round: int = 0
    verbose: bool

    def __init__(
        self,
        num_decks: int = 6,
        num_players: int = 6,
        min_bet: int = 10,
        verbose: bool = True,
    ):
        self.players = []
        self.min_bet = min_bet
        self.verbose = verbose

        self.standard_setup(num_players=num_players, num_decks=num_decks)

    def __str__(self) -> str:
        s = "" if len(self.players) == 1 else "s"
        return f"GameControl consisting of {len(self.players)} player{s}"

    def standard_setup(self, num_players: int, num_decks: int):
        self.add_deck(num_decks=num_decks)
        self.add_dealer()
        [self.add_player() for _ in range(num_players)]

    def add_deck(self, num_decks=6) -> deck_.Deck:
        assert not hasattr(self, "deck"), "A deck already exists in this game"
        new_deck = deck_.Deck(num_decks=num_decks)
        self.deck = new_deck
        return new_deck

    def add_dealer(self) -> participants.Dealer:
        assert not hasattr(self, "dealer"), "A dealer already exists in this game"
        new_dealer = participants.Dealer(game=self)
        self.dealer = new_dealer
        return new_dealer

    def add_player(self, name=None, money=500) -> participants.Player:
        if name in [p.name for p in self.players]:
            raise ValueError(f"The name {name} is already taken")
        new_player = participants.Player(game=self, name=name, money=money)
        self.players.append(new_player)
        return new_player

    def play_round(self):
        self.round += 1

        # place bets the deal
        [player.add_hand() for player in self.players]
        [player[0].deal() for player in self.players]
        self.dealer.hand.deal()

        print(self.dealer)
        for player in self.players:
            print(player)
            for hand in player.hands:
                hand.play_hand()  # TODO: implement this
