"""
Extend the ``playing_cards`` package with Blackjack-specific logic.
"""

from __future__ import annotations

import dataclasses
import functools
import itertools

import playing_cards


@functools.total_ordering
class Values:
    """
    Values for a playing card.
    """

    _values: set[int]

    def __init__(self, values: set[int]):
        self._values = values

    @classmethod
    def from_rank(cls, rank: playing_cards.Rank) -> Values:
        """
        Return a ``Value`` from a ``Rank``.
        """
        return cls(
            {1, 11} if rank == playing_cards.Rank.ACE else {min(rank.value, 10)}
        )

    def __str__(self):
        return str(self._values)

    def __repr__(self):
        return f"Value(value={self._values})"

    def __eq__(self, other: set[int] | Values) -> bool:
        if isinstance(other, Values):
            return self._values == other._values
        if isinstance(other, set):
            return self._values == other

        return NotImplemented

    def __lt__(self, other: Values) -> bool:
        return max(self._values) < max(other._values)

    def __iter__(self):
        yield from self._values

    def __add__(self, other: int | Values) -> Values:
        other_: set[int] = {other} if isinstance(other, int) else other._values
        if isinstance(other, int | Values):
            return Values(
                {sum(p) for p in itertools.product(self._values, other_)}
            )
        return NotImplemented

    def __radd__(self, other: int | Values) -> Values:
        return self + other

    @property
    def eligible_values(self) -> Values:
        """
        The eligible values for winning.
        """
        return Values({value for value in self._values if value <= 21})  # noqa: PLR2004


@dataclasses.dataclass
class Card(playing_cards.Card):
    """
    A playing card from the French-suited, standard 52-card pack.
    """

    values: Values = dataclasses.field(repr=False)

    def __init__(self, rank: playing_cards.Rank, suit: playing_cards.Suit):
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
