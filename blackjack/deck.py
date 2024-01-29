"""
Define the cards and decks.

A deck in the traditional sense is a collection of 52 playing cards from
the French-suited, standard 52-card pack.

A ``Deck`` in this module is ``n`` sets of decks (making it a slight
misnomer), where a ``Card`` class represents each playing card.

There are currently no Joker cards in the ``Card`` class.
"""

from __future__ import annotations

import dataclasses
import enum
import functools
import itertools
import pathlib
import random
import tomllib
from typing import Any, Literal

Colour = Literal["black", "red"]

_SUITS: dict[str, dict[str, str]] = tomllib.loads(
    pathlib.Path("blackjack/suits.toml").read_text(encoding="utf-8")
)
_RANKS: dict[str, dict[str, str]] = tomllib.loads(
    pathlib.Path("blackjack/ranks.toml").read_text(encoding="utf-8")
)


@functools.total_ordering
class Suit(enum.StrEnum):
    """
    A suit for a playing card.
    """

    CLUB = enum.auto()
    SPADE = enum.auto()
    HEART = enum.auto()
    DIAMOND = enum.auto()

    def __init__(self, *args, **kwargs):  # noqa: signature required for __new__
        assert self._get("_name")
        assert self._get("_value")

    def __lt__(self, other: Suit) -> bool:
        order = {
            Suit.CLUB: 0,
            Suit.DIAMOND: 1,
            Suit.HEART: 2,
            Suit.SPADE: 3,
        }
        return order[self] < order[other]

    def _get(self, _key: Any, /) -> Any:
        """
        Return the value of the key.
        """
        return _SUITS[self.value][_key]  # type: ignore

    @classmethod
    def from_id(cls, _id: str, /) -> Suit:
        """
        Return a ``Rank`` from its corresponding character.

        :raises KeyError: If the key does not correspond to a valid suit.
        """
        for suit, properties in _SUITS.items():
            if properties["id"] == _id:
                return cls(suit)

        raise KeyError(f"The key '{_id}' is not a valid suit")

    @property
    def id(self) -> str:
        """
        The single character corresponding to the suit.
        """
        return self._get("id")

    @property
    def image(self) -> str:
        """
        The image corresponding to the suit.
        """
        return self._get("image")

    @property
    def colour(self) -> Colour:
        """
        The colour corresponding to the suit.
        """
        return self._get("colour")


class Rank(enum.IntEnum):
    """
    A rank for a playing card.
    """

    ACE = enum.auto()
    TWO = enum.auto()
    THREE = enum.auto()
    FOUR = enum.auto()
    FIVE = enum.auto()
    SIX = enum.auto()
    SEVEN = enum.auto()
    EIGHT = enum.auto()
    NINE = enum.auto()
    TEN = enum.auto()
    JACK = enum.auto()
    QUEEN = enum.auto()
    KING = enum.auto()

    def __init__(self, *args, **kwargs):  # noqa: signature required for __new__
        assert self._get("_name")
        assert self._get("_value")

    def _get(self, _key: Any, /) -> Any:
        """
        Return the value of the key.
        """
        return _RANKS[str(self.value)][_key]  # type: ignore

    @classmethod
    def from_id(cls, _id: str, /) -> Rank:
        """
        Return a ``Rank`` from its corresponding character.
        """
        for rank, properties in _RANKS.items():
            if properties["id"] == _id:
                return cls(int(rank))

        raise KeyError(f"The key '{_id}' is not a valid rank")

    @property
    def id(self) -> str:
        """
        The single character corresponding to the rank.
        """
        return self._get("id")


@functools.total_ordering
class Values:
    """
    Values for a playing card.
    """

    _values: set[int]

    def __init__(self, values: set[int]):
        self._values = values

    @classmethod
    def from_rank(cls, rank: Rank) -> Values:
        """
        Return a ``Value`` from a ``Rank``.
        """
        return cls({1, 11} if rank == Rank.ACE else {min(rank.value, 10)})

    def __str__(self):
        return str(self._values)

    def __repr__(self):
        return f"Value(value={self._values})"

    def __eq__(self, other: set[int] | Values) -> bool:
        if isinstance(other, Values):
            return self._values == other._values
        elif isinstance(other, set):
            return self._values == other
        else:
            return NotImplemented

    def __lt__(self, other: Values) -> bool:
        return max(self._values) < max(other._values)

    def __iter__(self):
        yield from self._values

    def __add__(self, other: int | Values) -> Values:
        other_: set[int] = {other} if isinstance(other, int) else other._values
        if isinstance(other, (int, Values)):
            return Values({sum(p) for p in itertools.product(self._values, other_)})
        else:
            return NotImplemented

    def __radd__(self, other: int | Values) -> Values:
        return self + other

    @property
    def eligible_values(self) -> Values:
        """
        The eligible values for winning.
        """
        return Values({value for value in self._values if value <= 21})


@dataclasses.dataclass
class Card:
    """
    A playing card from the French-suited, standard 52-card pack.
    """

    rank: Rank
    suit: Suit
    values: Values = dataclasses.field(repr=False)

    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
        self.values = Values.from_rank(rank)

    def __str__(self):
        return self.rank.id + self.suit.id

    def __add__(self, other: int | Card) -> Values:
        """
        Return the sum of the two cards.
        """
        if isinstance(other, int):
            return self.values + other
        elif isinstance(other, Card):
            return self.values + other.values
        else:
            return NotImplemented

    def __radd__(self, other: int | Card) -> Values:
        return self + other

    @classmethod
    def from_str(cls, _key: str, /) -> Card:
        """
        Return a ``Card`` corresponding to the string.
        """
        if len(_key) != 2:
            raise KeyError(f"The key, {_key}, should be 2 characters")
        return cls(Rank.from_id(_key[0]), Suit.from_id(_key[1]))

    @property
    def face(self) -> str:
        """
        The face of the card.

        This shows the rank and then the image of the suit.
        """
        return self.rank.id + self.suit.image

    @property
    def colour(self) -> Colour:
        """
        The colour of the card.

        This is inherited from the suit.
        """
        return self.suit.colour


class Deck:
    """
    A class to represent a multiple sets of 52-card French-suited deck that
    may or may not have all cards in them.

    This name is a misnomer, since it can actually be many sets of decks
    (where "deck" means a set of 52 cards).
    """

    _num_decks: int
    cards: list[Card]

    def __init__(self, num_decks: int = 1):
        """
        Return a ``Deck`` with ``num_decks`` decks in it.

        :param num_decks: The number of 52-card decks to include.
        """
        self._num_decks = num_decks
        self.cards = []
        self.reset()

    def __str__(self):
        s = (
            "" if len(self) == 1 else "s"
        )  # sourcery skip: avoid-single-character-names-variables
        return f"Deck consisting of {len(self)} card{s}"

    def __repr__(self):
        return f"Deck(num_decks={self._num_decks})"

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]

    def reset(self) -> None:
        """
        Reset the deck to have all cards in it, then shuffle it.
        """
        self.cards = [
            Card(rank, suit)
            for _, rank, suit in itertools.product(range(self._num_decks), Rank, Suit)
        ]

        self.shuffle()

    def shuffle(self) -> None:
        """
        Shuffle the deck.
        """
        random.shuffle(self.cards)

    def take_card(self, _key: str = None) -> Card:
        """
        Return the top card from the deck.

        :param _key: The key of the card to take.

        :return: A list of the taken cards.
        """
        return self._take_card_by_key(_key) if _key else self.cards.pop()

    def _take_card_by_key(self, key: str) -> Card:
        """
        Pop the card from the deck whose key corresponds to ``key``.

        This is just for debugging and testing.

        :param key: The key of the card to take.

        :raises IndexError: If the card has already been removed from the deck.

        :return: A list of cards corresponding to the key.
        """
        for i, card in enumerate(self.cards):
            if str(card) == key:
                return self.cards.pop(i)
