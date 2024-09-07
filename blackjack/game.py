"""
Define the game.

This brings together the participants and the deck to play the game.
"""

from __future__ import annotations

from blackjack import constants, participants
from blackjack import deck as deck_


def play_hand(
    player_hand: participants.PlayerHand,
    game: Game,
    player: participants.Player,
) -> None:
    """
    Play the hand -- has three parts:

    1. player choices
    2. evaluate
    3. feedback
    """

    while player_hand.playing:
        print(f"\nPlaying hand {player_hand.show()!s}")

        options = game.get_player_options(player, player_hand)
        if not options:
            player_hand.playing = False
            break

        player_options = ", ".join(option.readable for option in options) + "?"
        decision = None
        while not decision:
            decision_key = input(f"{player_options} ")
            try:
                decision = participants.PlayerOption(decision_key)
                action(player_hand, decision, player, game.deck)
            except ValueError:
                print(f"Key {decision_key} not recognised, try again.")


def action(
    player_hand: participants.PlayerHand,
    option: participants.PlayerOption,
    player: participants.Player,
    deck: deck_.Deck,
) -> None:
    """
    Resolve the actions on the player given the option.

    :param player_hand: The hand the player is playing.
    :param option: The option the player has chosen.
    :param player: The player making the choice.
    :param deck: The deck to draw from.
    """
    match option:
        case participants.PlayerOption.TAKE_INSURANCE:
            # TODO: Update their bet and money
            player_hand.playing = False
        case participants.PlayerOption.HIT:
            player_hand.hit(deck)
        case participants.PlayerOption.STAND:
            player_hand.playing = False
        case participants.PlayerOption.DOUBLE_DOWN:
            player_hand.hit(deck)
            player_hand.playing = False
        case participants.PlayerOption.SPLIT:
            player_hand.split(deck, player)


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
        self, number_of_players: int, number_of_decks: int
    ) -> None:
        """
        Set up a standard game of Blackjack.

        :param number_of_players: The number of players to add to the game.
        :param number_of_decks: The number of 52-card decks to use in the game.
        """
        self.add_deck(number_of_decks)
        self.add_dealer()
        [self.add_player(f"Player_{i}", 500) for i in range(number_of_players)]

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
        for player in self.players:
            print(player.name_and_money)
            for hand in player.hands:
                play_hand(hand, self, player)

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
        self,
        hand: participants.Hand,
        player: participants.Player,
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
        print(f"Outcome: {hand.outcome.formatted}")

    def get_player_options(
        self,
        player: participants.Player,
        hand: participants.Hand,
    ) -> list[participants.PlayerOption]:
        """
        Options to give the player when playing their hand.

        :return: The list of the options to give.
        """
        if hand.bust:
            return []
        if hand.blackjack:
            if self.dealer.hand.cards[0].rank == 1:
                return [
                    participants.PlayerOption.TAKE_INSURANCE,
                    participants.PlayerOption.STAND,
                    participants.PlayerOption.HIT,
                    participants.PlayerOption.DOUBLE_DOWN,
                ]
            return []
        if len(hand) == 2 and player.money > hand.bet:  # noqa: PLR2004
            if hand[0].rank == hand[1].rank:
                return [
                    participants.PlayerOption.STAND,
                    participants.PlayerOption.HIT,
                    participants.PlayerOption.DOUBLE_DOWN,
                    participants.PlayerOption.SPLIT,
                ]
            return [
                participants.PlayerOption.STAND,
                participants.PlayerOption.HIT,
                participants.PlayerOption.DOUBLE_DOWN,
            ]
        return [participants.PlayerOption.STAND, participants.PlayerOption.HIT]
