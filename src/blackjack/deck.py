"""
Extend the ``playing_cards`` package with Blackjack-specific logic.
"""

from __future__ import annotations

import dataclasses
import functools
import itertools
from collections.abc import Generator

import playing_cards

from blackjack import constants


@functools.total_ordering
class Values:
    """
    Values for a playing card.

    Usually, a playing card's value is the same as its rank. However, an ace
    can have a value of 1 and 11, and face cards have a value of 10.
    """

    _values: set[int]

    def __init__(self, values: set[int]) -> None:
        self._values = values

    @classmethod
    def from_rank(cls, rank: playing_cards.Rank) -> Values:
        """
        Return a ``Value`` from a ``Rank``.
        """
        return cls(
            {1, 11} if rank == playing_cards.Rank.ACE else {min(rank.value, 10)}
        )

    def __str__(self) -> str:
        return str(self._values) if self._values else "BUST!"

    def __repr__(self) -> str:
        return f"Value(value={self._values})"

    def __hash__(self) -> int:
        return hash(frozenset(self._values))

    def __eq__(self, other: Values) -> bool:
        if isinstance(other, Values):
            return self._values == other._values
        return NotImplemented

    def __lt__(self, other: Values) -> bool:
        return max(self._values) < max(other._values)

    def __add__(self, other: int | Values) -> Values:
        if isinstance(other, int):
            other_ = {other}
        elif isinstance(other, Values):
            other_ = other._values
        else:
            return NotImplemented

        return Values({sum(p) for p in itertools.product(self._values, other_)})

    def __iter__(self) -> Generator[int]:
        yield from self._values

    @property
    def eligible_values(self) -> Values:
        """
        The eligible values for winning.
        """
        return Values(
            {value for value in self._values if value <= constants.BLACKJACK}
        )


@dataclasses.dataclass
class Card(playing_cards.Card):
    """
    A playing card from the French-suited, standard 52-card pack.
    """

    values: Values = dataclasses.field(repr=False)

    def __init__(
        self,
        rank: playing_cards.Rank,
        suit: playing_cards.Suit,
    ) -> None:
        self.rank = rank
        self.suit = suit
        self.values = Values.from_rank(rank)

    def __add__(self, other: int | Card) -> Values:
        """
        Return the sum of the two cards.
        """
        if isinstance(other, int):
            return self.values + other
        if isinstance(other, Card):
            return self.values + other.values
        return NotImplemented

    def __radd__(self, other: int | Card) -> Values:
        return self + other

    @property
    def face(self) -> str:
        """
        The face of the card.
        """
        face = super().face
        if self.suit in {playing_cards.Suit.HEART, playing_cards.Suit.DIAMOND}:
            return f"{constants.Colours.RED}{face}{constants.Colours.END}"
        return f"{constants.Colours.BLUE}{face}{constants.Colours.END}"


class Deck(playing_cards.Decks):
    """
    A set of multiple decks of cards.
    """

    def reset(self) -> None:
        """
        Reset the deck to have all cards in it, then shuffle it.
        """
        rank: playing_cards.Rank  # noqa: F842
        suit: playing_cards.Suit  # noqa: F842
        self.cards = [
            Card(rank, suit)
            for _, rank, suit in itertools.product(
                range(self.number_of_decks),
                playing_cards.Rank,
                playing_cards.Suit,
            )
        ]

        self.shuffle()
