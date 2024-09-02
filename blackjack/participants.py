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


class Hand(abc.ABC):
    """
    A hand, which holds cards.
    """

    game: blackjack.Game
    participant: Participant
    cards: list[blackjack.Card]
    playing: bool = True

    def __init__(self, game: blackjack.Game, participant: Participant):
        """
        Instantiate a hand for a participant in a game.

        :param participant: The participant that the hand belongs to.
        """
        self.game = game
        self.participant = participant
        self.cards = []

    @classmethod
    def from_participant(cls, participant: Participant) -> Hand:
        """
        Instantiate a hand for a participant in a game.

        :param participant: The participant that the hand belongs to.
        """
        return cls(game=participant.game, participant=participant)

    def __str__(self) -> str:
        faces = " ".join(str(card) for card in self.cards)
        return f"[{faces}] {self.values.eligible_values}"

    def __repr__(self) -> str:
        return f"Hand(player='{self.participant}')"

    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, position: int) -> blackjack.Card:
        return self.cards[position]

    @property
    def values(self) -> blackjack.Values:
        """
        The set-value of the hand accounting for Aces.
        """
        if self.cards:
            return sum(card.values for card in self.cards)  # type: ignore
        return blackjack.Values({0})

    @property
    def blackjack(self) -> bool:
        """
        Whether the hand is a blackjack (21 with two cards).
        """
        return len(self) == 2 and max(self.values.eligible_values) == 21  # noqa: PLR2004

    @property
    def bust(self) -> bool:
        """
        Whether the hand is a bust (over 21).
        """
        return min(self.values) > 21  # noqa: PLR2004

    def hit(self, _key: str | None = None) -> None:
        """
        Take a card from the deck and add it to the hand.
        """
        self.cards.append(self.game.deck.take_card(_key))

    def deal(self, _keys: list[str] | None = None) -> None:
        """
        Deal two cards to the hand from the deck.
        """
        assert len(self) == 0, "This hand has already been dealt to"  # noqa: S101
        if _keys:
            assert len(_keys) == 2, "Can only deal two cards"  # noqa: S101,PLR2004
            [self.hit(key) for key in _keys]
        else:
            self.hit(), self.hit()

    def show_cards(self) -> None:
        """
        Print the cards in the hand to the terminal in a human-readable way.
        """
        print(f"{self.participant.name}'s hand:    {self}")

    @abc.abstractmethod
    def evaluate(self) -> None:
        """
        Evaluate the hand and update the outcome.

        TODO: Rename this to ``play_hand()`` and split the play from the
              evaluation.
        """


class DealerHand(Hand):
    """
    A class to represent the House dealer in Blackjack. Inherits Hand
    """

    participant: Dealer

    def __str__(self):
        return self.masked_cards if self.playing else super().__str__()

    @property
    def masked_cards(self) -> str:
        """
        Return the cards in the hand, with the first masked.
        """
        return f"[{self.cards[0]} ??] [{self.cards[0].values}]\n"

    def evaluate(self) -> None:
        """
        Play the dealer's hand.

        The dealer must hit on 16 or less and stand on 17 or more.
        """
        assert len(self) == 2, "Dealer must have two cards to play"  # noqa: S101,PLR2004
        while max(self.values) < 17:  # noqa: PLR2004
            self.hit()
        self.playing = False


class PlayerHand(Hand):
    """
    A player's hand(s) in Blackjack.
    """

    participant: Player
    bet: int
    outcome: PlayerOutcome
    from_split: bool

    def __init__(self, player: Player, bet: int):
        # I think this violates the Liskov substitution principle
        super().__init__(game=player.game, participant=player)

        self.bet = bet
        self.from_split = False

    @property
    def options(self) -> list[PlayerOption]:
        """
        Options to give the player when playing their hand.

        :return: The list of the options to give.
        """
        if self.bust:
            return []
        if self.blackjack:
            if self.participant.game.dealer.hand.cards[0].rank == 1:
                return [
                    PlayerOption.TAKE_INSURANCE,
                    PlayerOption.STAND,
                    PlayerOption.HIT,
                    PlayerOption.DOUBLE_DOWN,
                ]
            return []
        if len(self) == 2 and self.participant.money > self.bet:  # noqa: PLR2004
            if self[0].rank == self[1].rank:
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

    def play_hand(self) -> None:
        """
        Play the hand -- has three parts:

        1. player choices
        2. evaluate
        3. feedback
        """
        # Split from Ace's should never come down here
        if self.from_split:
            assert self[0].rank != 1  # noqa: S101
            assert self[1].rank != 1  # noqa: S101

        while self.playing:
            print(f"Playing hand {self!s}")

            options = self.options
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
                    decision.action(self)
                except ValueError:
                    print(f"Key {decision_key} not recognised, try again.")

    def evaluate(self) -> None:
        """
        Evaluate the hand and update the outcome.
        """
        dealer = self.participant.game.dealer
        hand_value = max(
            self.values if self.bust else self.values.eligible_values
        )
        dealer_value = max(dealer.hand.values)

        if self.bust:
            self.outcome = PlayerOutcome.LOSE
        elif dealer.hand.blackjack:
            if self.blackjack:
                self.outcome = PlayerOutcome.DRAW
            else:
                # Assuming that dealer blackjack beats player 21
                print("Dealer has blackjack")
                self.outcome = PlayerOutcome.LOSE
        elif dealer.hand.bust:
            self.outcome = PlayerOutcome.WIN
        elif hand_value < dealer_value:
            self.outcome = PlayerOutcome.LOSE
        elif hand_value == dealer_value:
            self.outcome = PlayerOutcome.DRAW
        elif hand_value > dealer_value:
            self.outcome = PlayerOutcome.WIN
        else:
            raise ValueError(
                f"Unexpected state: {hand_value=}, {dealer_value=}"
            )

        self.show_cards()
        print(f"Outcome: {self.outcome.value}")

    def split(self) -> None:
        """
        Split the hand into two hands.
        """
        # fmt: off
        assert len(self) == 2, f"Can't split a hand with {len(self)} cards"  # noqa: S101,PLR2004
        assert (self[0].rank == self[1].rank), f"Can't split a hand with cards {self[0]} and {self[1]}"  # noqa: S101
        # fmt: on

        new_hand = self.participant.add_hand(bet=self.bet)
        new_hand.cards.append(self.cards.pop(1))
        new_hand.from_split = True
        self.hit(), new_hand.hit()

        if self[0].rank == 1:
            # Splitting Ace's only gets one card each
            self.playing = False
            new_hand.playing = False


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

    def action(self, player_hand: PlayerHand) -> None:
        """
        Resolve the actions on the player given the option.

        :param player_hand: The player's hand to resolve the action on.
        """
        match self:
            case PlayerOption.TAKE_INSURANCE:
                # TODO: Update their bet and money
                player_hand.playing = False
            case PlayerOption.HIT:
                player_hand.hit()
            case PlayerOption.STAND:
                player_hand.playing = False
            case PlayerOption.DOUBLE_DOWN:
                player_hand.hit()
                player_hand.playing = False
            case PlayerOption.SPLIT:
                player_hand.split()


class PlayerOutcome(enum.Enum):
    """
    Outcomes for the player in a game of Blackjack.
    """

    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"


class Participant(abc.ABC):
    """
    A participant in a game of Blackjack.
    """

    game: blackjack.Game
    name: str

    def __init__(self, game: blackjack.Game, name: str):
        """
        Instantiate a participant in a game of Blackjack.

        :param game: The game in play.
        :param name: The name of the participant.
        """
        self.game = game
        self.name = name

    def __str__(self) -> str:
        return self.name


class Dealer(Participant):
    """
    The dealer in a game of Blackjack.
    """

    hand: DealerHand

    def __init__(self, game: blackjack.Game):
        # I think this violates the Liskov substitution principle
        super().__init__(game=game, name="Dealer")
        self.hand = DealerHand.from_participant(self)

    def play_hand(self) -> None:
        """
        Play the dealer's hand.
        """
        self.hand.evaluate()


class Player(Participant):
    """
    A player in a game of Blackjack.
    """

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
        # I think this violates the Liskov substitution principle
        super().__init__(
            game=game, name=name or f"Player_{1 + len(game.players)}"
        )
        self.hands = []
        self.money = money

    def __len__(self):
        return len(self.hands)

    def __getitem__(self, position):
        return self.hands[position]

    def add_hand(self, bet: float | None = None) -> PlayerHand:
        """
        Add a hand to the player.
        """
        # TODO: Bet should be a player attribute so that additional hands' bets
        #       can be inferred from the previous hand
        stake = bet or self.game.min_bet
        new_hand = PlayerHand(player=self, bet=stake)
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
            description += f"\n    {hand}  stake: £{hand.bet}"

        return description + "\n"
