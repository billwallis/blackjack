"""
Define the game.

This brings together the participants and the deck to play the game.
"""

from __future__ import annotations

from blackjack import deck as deck_
from blackjack import participants, rules


class Game:
    """
    A class to control the Blackjack game.
    """

    min_bet: int
    round: int
    deck: deck_.Deck
    dealer: participants.Dealer
    players: list[participants.Player]

    def __init__(self, min_bet: int):
        self.min_bet = min_bet
        self.round = 0
        self.players = []

    def __str__(self) -> str:
        # sourcery skip: avoid-single-character-names-variables
        s = "" if len(self.players) == 1 else "s"
        return f"Game consisting of {len(self.players)} player{s}"

    def standard_setup(
        self,
        number_of_players: int,
        number_of_decks: int,
    ) -> None:
        """
        Set up a standard game of Blackjack.

        :param number_of_players: The number of players to add to the game.
        :param number_of_decks: The number of 52-card decks to use in the game.
        """
        self.add_deck(number_of_decks)
        self.add_dealer()
        [
            self.add_player(f"Player_{i + 1}", 500)
            for i in range(number_of_players)
        ]

    def add_deck(self, number_of_decks: int) -> deck_.Deck:
        """
        Add a stack of deck to the game.

        :param number_of_decks: The number of 52-card decks to add.

        :return: The stack of decks for the game.
        """
        if hasattr(self, "deck"):
            raise AssertionError("A deck already exists in this game")

        self.deck = deck_.Deck(number_of_decks)
        return self.deck

    def add_dealer(self) -> participants.Dealer:
        """
        Add a dealer to the game.

        :return: The dealer for the game.
        """
        if hasattr(self, "dealer"):
            raise AssertionError("A dealer already exists in this game")

        self.dealer = participants.Dealer()
        return self.dealer

    def add_player(self, name: str, money: int) -> participants.Player:
        """
        Add a player to the game.

        :param name: The name of the player.
        :param money: The amount of money the player has.

        :return: The player added to the game.
        """
        if name in [p.name for p in self.players]:
            raise ValueError(f"The name {name} is already taken")

        new_player = participants.Player(name, money)
        self.players.append(new_player)

        return new_player

    def reset_round(self) -> None:
        """
        Reset the game for a new round.
        """
        self.round = 0
        self.deck.reset()
        self.dealer.hand.cards = []
        for player in self.players:
            player.hands = []

    def play_round(self) -> None:
        """
        Play a round of Blackjack.

        TODO: Improve the feedback loop.
        """
        self.round += 1

        # Place bets, then deal
        [player.add_hand(self.min_bet) for player in self.players]
        [player.hands[0].deal(self.deck) for player in self.players]
        self.dealer.hand.deal(self.deck)

        print(self.dealer, self.dealer.hand.show(masked=True), sep="\n")
        print()
        for player in self.players:
            print(player.name_and_money, "\n")

        for player in self.players:
            print(f"\n{player.name}'s turn:")
            for hand in player.hands:
                rules.play_hand__player(
                    hand,
                    self.dealer.hand,
                    player,
                    self.deck,
                )

        rules.play_hand__dealer(self.dealer.hand, self.deck)
        print()
        print(self.dealer.name, self.dealer.hand.show())
        print()
        for player in self.players:
            for hand in player.hands:
                outcome = rules.get_hand_outcome(hand, self.dealer.hand)
                print()
                print(player.name, hand.show())
                print(f"Outcome: {outcome.formatted}")
                rules.apply_outcome(player, outcome, hand.bet)
