# sourcery skip: avoid-single-character-names-variables
"""
Define the game.

This brings together the participants and the deck to play the game.
"""

from __future__ import annotations

from blackjack import constants, participants
from blackjack import deck as deck_


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
        min_bet: int = 10,
    ):
        self.players = []
        self.min_bet = min_bet

    def __str__(self) -> str:
        s = "" if len(self.players) == 1 else "s"
        return f"Game consisting of {len(self.players)} player{s}"

    def standard_setup(self, num_players: int, num_decks: int) -> None:
        """
        Set up a standard game of Blackjack.

        :param num_players: The number of players to add to the game.
        :param num_decks: The number of decks to use in the game.
        """
        self.add_deck(num_decks=num_decks)
        self.add_dealer()
        [self.add_player(f"Player_{i}") for i in range(num_players)]

    def add_deck(self, num_decks: int) -> deck_.Deck:
        """
        Add a stack of deck to the game.

        :param num_decks: The number of decks to add.
        :return: The stack of decks for the game.
        """
        assert not hasattr(self, "deck"), "A deck already exists in this game"  # noqa: S101

        new_deck = deck_.Deck(num_decks)
        self.deck = new_deck

        return new_deck

    def add_dealer(self) -> participants.Dealer:
        """
        Add a dealer to the game.

        :return: The dealer for the game.
        """
        assert not hasattr(  # noqa: S101
            self, "dealer"
        ), "A dealer already exists in this game"

        new_dealer = participants.Dealer()
        self.dealer = new_dealer

        return new_dealer

    def add_player(self, name: str, money: int = 500) -> participants.Player:
        """
        Add a player to the game.

        :param name: The name of the player.
        :param money: The amount of money the player has.

        :return: The player added to the game.
        """
        if name in [p.name for p in self.players]:
            raise ValueError(f"The name {name} is already taken")

        new_player = participants.Player(game=self, name=name, money=money)
        self.players.append(new_player)

        return new_player

    def play_round(self) -> None:
        """
        Play a round of Blackjack.

        TODO: Improve the feedback loop.
        """
        self.round += 1

        # Place bets, then deal
        [player.add_hand(self.min_bet) for player in self.players]
        [player[0].deal(self.deck) for player in self.players]
        self.dealer.hand.deal(self.deck)

        print(self.dealer, self.dealer.hand.show(masked=True), sep="\n")
        for player in self.players:
            print(player.name_and_money)
            for hand in player.hands:
                hand.play_hand(self, player)

        self.evaluate_dealer()
        print()
        print(self.dealer.name, self.dealer.hand.show())
        for player in self.players:
            for hand in player.hands:
                self.evaluate_player(hand, player)

    def evaluate_dealer(self) -> None:
        """
        Play the dealer's hand.

        The dealer must hit on 16 or less and stand on 17 or more.
        """
        while max(self.dealer.hand.values) < constants.DEALER_LOWER_LIMIT:
            self.dealer.hand.hit(self.deck)
        self.dealer.hand.playing = False

    def evaluate_player(
        self, hand: participants.Hand, player: participants.Player
    ) -> None:
        """
        Evaluate the hand and update the outcome.
        """
        hand_value = max(
            hand.values if hand.bust else hand.values.eligible_values
        )
        dealer_value = max(
            (
                value
                for value in self.dealer.hand.values
                if value <= constants.BLACKJACK
            ),
            default=99,
        )

        if hand.bust:
            hand.outcome = participants.PlayerOutcome.LOSE
        elif self.dealer.hand.blackjack:
            if hand.blackjack:
                hand.outcome = participants.PlayerOutcome.DRAW
            else:
                # Assuming that dealer blackjack beats player 21
                print("Dealer has blackjack")
                hand.outcome = participants.PlayerOutcome.LOSE
        elif self.dealer.hand.bust:
            hand.outcome = participants.PlayerOutcome.WIN
        elif hand_value < dealer_value:
            hand.outcome = participants.PlayerOutcome.LOSE
        elif hand_value == dealer_value:
            hand.outcome = participants.PlayerOutcome.DRAW
        elif hand_value > dealer_value:
            hand.outcome = participants.PlayerOutcome.WIN

        print()
        print(player.name, hand.show())
        print(f"Outcome: {hand.outcome.value}")
