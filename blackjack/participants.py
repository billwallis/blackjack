# sourcery skip: avoid-single-character-names-variables
"""
Define the participants in the game.

This includes the dealer (AKA "the house") and the players, both of
which have a corresponding hand that holds some cards.
"""

from __future__ import annotations

import abc
import enum

import blackjack
from blackjack import constants
from blackjack import deck as deck_


class PlayerOutcome(enum.Enum):
    """
    Outcomes for the player in a game of Blackjack.
    """

    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"


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


class Hand(abc.ABC):
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
            return sum(card.values for card in self.cards)  # type: ignore
        return deck_.Values({0})

    @property
    def blackjack(self) -> bool:
        """
        Whether the hand is a blackjack.
        """
        return (
            len(self) == constants.BLACKJACK_CARDS
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
        """
        self.cards.append(deck.take_card(_key))

    def deal(self, deck: deck_.Deck, _keys: list[str] | None = None) -> None:
        """
        Deal two cards to the hand from the deck.
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
        """
        if masked:
            return f"[{self.cards[0].face} ??] [{self.cards[0].values}]\n"

        faces = " ".join(card.face for card in self.cards)
        return f"[{faces}] {self.values.eligible_values}"


class PlayerHand(Hand):
    """
    A player's hand(s) in Blackjack.
    """

    outcome: PlayerOutcome
    from_split: bool = False

    def play_hand(self, game: blackjack.Game, player: Player) -> None:
        """
        Play the hand -- has three parts:

        1. player choices
        2. evaluate
        3. feedback
        """

        while self.playing:
            print(f"\nPlaying hand {self.show()!s}")

            options = get_options(player, self, game)
            if not options:
                self.playing = False
                break

            player_options = (
                ", ".join(option.readable for option in options) + "?"
            )
            decision = None
            while not decision:
                decision_key = input(f"{player_options} ")
                try:
                    decision = PlayerOption(decision_key)
                    self.action(decision, player, game.deck)
                except ValueError:
                    print(f"Key {decision_key} not recognised, try again.")

    def action(
        self,
        option: PlayerOption,
        player: Player,
        deck: deck_.Deck,
    ) -> None:
        """
        Resolve the actions on the player given the option.

        :param option: The option the player has chosen.
        :param player: The player making the choice.
        :param deck: The deck to draw from.
        """
        match option:
            case PlayerOption.TAKE_INSURANCE:
                # TODO: Update their bet and money
                self.playing = False
            case PlayerOption.HIT:
                self.hit(deck)
            case PlayerOption.STAND:
                self.playing = False
            case PlayerOption.DOUBLE_DOWN:
                self.hit(deck)
                self.playing = False
            case PlayerOption.SPLIT:
                self.split(deck, player)

    def split(self, deck: deck_.Deck, player: Player) -> None:
        """
        Split the hand into two hands.
        """
        # fmt: off
        assert len(self) == 2, f"Can't split a hand with {len(self)} cards"  # noqa: S101,PLR2004
        assert (self[0].rank == self[1].rank), f"Can't split a hand with cards {self[0]} and {self[1]}"  # noqa: S101
        # fmt: on

        new_hand = player.add_hand(bet=self.bet)
        new_hand.cards.append(self.cards.pop(1))
        new_hand.from_split = True
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
    insurance: float = 0  # TODO: need to include insurance somewhere

    def __init__(
        self,
        game: blackjack.Game,
        name: str | None = None,
        money: float = 500,
    ):
        """
        Instantiate a player in a game of Blackjack.

        :param game: The game in play.
        :param name: The name of the player.
        :param money: The amount of money the player has.
        """
        self.hands = []
        self.money = money
        self.name = name or f"Player_{1 + len(game.players)}"

    def __len__(self):
        return len(self.hands)

    def __str__(self) -> str:
        return self.name

    def __getitem__(self, position):
        return self.hands[position]

    def add_hand(self, bet: int) -> PlayerHand:
        """
        Add a hand to the player.
        """
        # TODO: Bet should be a player attribute so that additional hands' bets
        #       can be inferred from the previous hand
        new_hand = PlayerHand(bet=bet)
        self.hands.append(new_hand)

        return new_hand

    def clear_hands(self) -> None:
        """
        Clear the player's hands.
        """
        self.hands = []

    def add_money(self, amount: float) -> None:
        """
        Add money to the player's total.
        """
        self.money += amount
        outcome = ["won", "lost"][amount < 0]
        print(f"{self.name} {outcome} {abs(amount)}")

    def print_money(self) -> None:
        """
        Print the player's money.
        """
        print(f"{self.name} has {self.money!s} money")

    @property
    def name_and_money(self) -> str:
        """
        Return the player's name and money.
        """
        s = "s" if len(self) != 1 else ""
        description = f"{self.name} has £{self.money} with hand{s}:"
        for hand in self.hands:
            description += f"\n    {hand.show()}  stake: £{hand.bet}"

        return description


def get_options(
    player: Player, hand: Hand, game: blackjack.Game
) -> list[PlayerOption]:
    """
    Options to give the player when playing their hand.

    :return: The list of the options to give.
    """
    if hand.bust:
        return []
    if hand.blackjack:
        if game.dealer.hand.cards[0].rank == 1:
            return [
                PlayerOption.TAKE_INSURANCE,
                PlayerOption.STAND,
                PlayerOption.HIT,
                PlayerOption.DOUBLE_DOWN,
            ]
        return []
    if len(hand) == 2 and player.money > hand.bet:  # noqa: PLR2004
        if hand[0].rank == hand[1].rank:
            return [
                PlayerOption.STAND,
                PlayerOption.HIT,
                PlayerOption.DOUBLE_DOWN,
                PlayerOption.SPLIT,
            ]
        return [
            PlayerOption.STAND,
            PlayerOption.HIT,
            PlayerOption.DOUBLE_DOWN,
        ]
    return [PlayerOption.STAND, PlayerOption.HIT]
