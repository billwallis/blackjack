"""
Define the participants in the game.

This includes the dealer (AKA "the house") and the players, both of
which have a corresponding hand that holds some cards.
"""

from __future__ import annotations

import enum

from blackjack import constants
from blackjack import deck as deck_


class HandOutcome(enum.StrEnum):
    """
    Outcomes for the player in a game of Blackjack.
    """

    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"

    @property
    def formatted(self) -> str:
        """
        Return a formatted version of the outcome.
        """
        outcome = {
            HandOutcome.WIN: f"{constants.Colours.PASS}win",
            HandOutcome.LOSE: f"{constants.Colours.FAIL}lose",
            HandOutcome.DRAW: f"{constants.Colours.WARN}draw",
        }[self]
        return constants.Colours.BOLD + outcome + constants.Colours.END


class PlayerOption(enum.Enum):
    """
    Options that a player can take in a game of Blackjack.
    """

    HIT = "h"
    STAND = "s"
    DOUBLE_DOWN = "d"
    SPLIT = "sp"
    TAKE_INSURANCE = "t"

    @property
    def readable(self) -> str:
        """
        Return a human-readable version of the option.
        """
        pretty_name = self.name.replace("_", " ").capitalize()

        return f"[{self.value}] {pretty_name}"


class Hand:
    """
    A hand, which holds cards.
    """

    cards: list[deck_.Card]
    bet: int | None
    playing: bool = True

    def __init__(self, bet: int | None):
        self.bet = bet
        self.cards = []

    def __str__(self) -> str:
        return self.show()

    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, position: int) -> deck_.Card:
        return self.cards[position]

    @property
    def values(self) -> deck_.Values:
        """
        The set-value of the hand accounting for Aces.
        """
        if self.cards:
            # `start` tells the typing system that the return value is `Values`
            return sum(
                (card.values for card in self.cards),
                start=deck_.Values({0}),
            )
        return deck_.Values({0})

    @property
    def blackjack(self) -> bool:
        """
        Whether the hand is a blackjack.
        """
        return (
            len(self) == constants.BLACKJACK_CARD_COUNT
            and max(self.values.eligible_values) == constants.BLACKJACK
        )

    @property
    def bust(self) -> bool:
        """
        Whether the hand is a bust.
        """
        return min(self.values) > constants.BLACKJACK

    def hit(self, deck: deck_.Deck, _key: str | None = None) -> None:
        """
        Take a card from the deck and add it to the hand.

        :param deck: The deck to take the card from.
        :param _key: The key of the card to take (for testing only).
        """
        self.cards.append(deck.take_card(_key))

    def deal(self, deck: deck_.Deck, _keys: list[str] | None = None) -> None:
        """
        Deal two cards to the hand from the deck.

        :param deck: The deck to deal from.
        :param _keys: The keys of the cards to deal (for testing only).
        """
        if len(self) != 0:
            raise ValueError("Hand already has cards")

        if _keys:
            [self.hit(deck, key) for key in _keys]
        else:
            self.hit(deck), self.hit(deck)

    def show(self, masked: bool = False) -> str:
        """
        Show the cards in the hand.

        :param masked: Whether to show the first card masked.

        :return: The string representation of the hand.
        """
        if masked:
            return f"[{self.cards[0].face} ??] [{self.cards[0].values}]"

        faces = " ".join(card.face for card in self.cards)
        return f"[{faces}] {self.values.eligible_values}"


class PlayerHand(Hand):
    """
    A player's hand in Blackjack.
    """

    from_split: bool
    insurance: int  # TODO: need to include insurance somewhere

    def __init__(self, bet: int, from_split: bool):
        self.from_split = from_split
        self.insurance = 0
        super().__init__(bet)

    def split(self, deck: deck_.Deck, player: Player) -> None:
        """
        Split the hand into two hands.
        """
        new_hand = player.add_hand(bet=self.bet, from_split=True)
        new_hand.cards.append(self.cards.pop(1))
        new_hand.from_split = True
        self.from_split = True
        self.hit(deck), new_hand.hit(deck)

        if self[0].rank == 1:
            # Splitting Ace's only gets one card each
            self.playing = False
            new_hand.playing = False


class Dealer:
    """
    The dealer in a game of Blackjack.
    """

    name: str
    hand: Hand

    def __init__(self):
        self.name = "Dealer"
        self.hand = Hand(bet=None)

    def __str__(self) -> str:
        return self.name


class Player:
    """
    A player in a game of Blackjack.
    """

    name: str
    hands: list[PlayerHand]
    money: float

    def __init__(self, name: str, money: int):
        """
        Instantiate a player in a game of Blackjack.

        :param name: The name of the player.
        :param money: The amount of money the player has.
        """
        self.name = name
        self.money = money
        self.hands = []

    def __str__(self) -> str:
        return self.name

    def __len__(self):
        return len(self.hands)

    @property
    def name_and_money(self) -> str:
        """
        Return the player's name and money.
        """
        # sourcery skip: avoid-single-character-names-variables
        s = "s" if len(self) != 1 else ""
        description = f"{self.name} has £{self.money} with hand{s}:"
        for hand in self.hands:
            description += f"\n    {hand.show()}  stake: £{hand.bet}"

        return description

    def add_hand(self, bet: int, from_split: bool = False) -> PlayerHand:
        """
        Add a hand to the player.
        """
        # TODO: Bet should be a player attribute so that additional hands' bets
        #       can be inferred from the previous hand  -->  players make a bet
        #       before getting a hand, anyway
        new_hand = PlayerHand(bet, from_split)
        self.hands.append(new_hand)

        return new_hand
