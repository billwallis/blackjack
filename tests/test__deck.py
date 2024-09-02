"""
Test the ``blackjack.deck`` module.
"""

import playing_cards
import pytest

from blackjack import deck


###
# Value tests
###
def test__values():
    """
    Test the construction of the ``Values`` class.
    """
    value = deck.Values({1, 11})
    assert value._values == {1, 11}


def test__values__str():
    """
    Test the ``Values.__str__()`` and ``Values.__repr__()`` methods.
    """
    value = deck.Values({1, 11})
    assert str(value) == "{1, 11}"
    assert repr(value) == f"Value(value={value._values})"


@pytest.mark.parametrize(
    "values_1, values_2, expected",
    [
        ({1}, {2}, True),
        ({2}, {1}, False),
        ({3}, {1, 5}, True),
        ({2}, {1, 3}, True),
        ({1, 2}, {2, 3}, True),
        ({1, 3}, {2}, False),
        ({1, 2, 3}, {4}, True),
    ],
)
def test__values__lt(values_1: set[int], values_2: set[int], expected: bool):
    """
    Test the ``Values.__lt__()`` method.
    """
    value_1 = deck.Values(values_1)
    value_2 = deck.Values(values_2)
    assert (value_1 < value_2) is expected


def test__values__eq():
    """
    Test the ``Values.__eq__()`` method.
    """
    value_1 = deck.Values({1})
    value_2 = deck.Values({1})
    assert value_1 == value_2


def test__values__not_implemented():
    """
    Test that the ``Values.__eq__()`` method throws an exception.
    """
    assert (deck.Values({1}) == "one") is False


@pytest.mark.parametrize(
    "values_1, values_2, result",
    [
        ({1}, {2}, {3}),
        ({2}, {1}, {3}),
        ({3}, {1, 5}, {4, 8}),
        ({2}, {1, 3}, {3, 5}),
        ({1, 2}, {2, 3}, {3, 4, 5}),
        ({1, 2, 3}, {4}, {5, 6, 7}),
        ({10}, {1, 11}, {11, 21}),
        ({1, 11}, {11, 21}, {12, 22, 32}),
    ],
)
def test__values__add(
    values_1: set[int],
    values_2: set[int],
    result: set[int],
):
    """
    Test the ``Values.__add__()`` method.
    """
    value_1 = deck.Values(values_1)
    value_2 = deck.Values(values_2)
    assert value_1 + value_2 == result


@pytest.mark.parametrize(
    "values, eligible_values",
    [
        ({1}, {1}),
        ({1, 11}, {1, 11}),
        ({30}, set()),
        ({1, 11, 30}, {1, 11}),
        ({12, 22, 32}, {12}),
    ],
)
def test__values__eligible_values(values: set[int], eligible_values: set[int]):
    """
    Test the ``Values.eligible_values`` property.
    """
    assert deck.Values(values).eligible_values == deck.Values(eligible_values)


###
# Card tests
###
@pytest.mark.parametrize(
    "card, other, result",
    [
        (deck.Card.from_id("2S"), deck.Card.from_id("TC"), {12}),
        (deck.Card.from_id("TC"), deck.Card.from_id("TC"), {20}),
        (deck.Card.from_id("2S"), 10, {12}),
        (deck.Card.from_id("TC"), 10, {20}),
    ],
)
def test__card__add(card: deck.Card, other: int | deck.Card, result: set[int]):
    """
    Test the ``Card.__add__()`` method.
    """
    assert card + other == result
    assert other + card == result


def test__card__add__raises():
    """
    Test that ``Card.__add__()`` raises a ``TypeError``.
    """
    with pytest.raises(TypeError):
        deck.Card.from_id("2S") + "2"  # type: ignore


@pytest.mark.parametrize(
    "rank, values",
    [
        (playing_cards.Rank.ACE, {1, 11}),
        (playing_cards.Rank.TWO, {2}),
        (playing_cards.Rank.THREE, {3}),
        (playing_cards.Rank.FOUR, {4}),
        (playing_cards.Rank.FIVE, {5}),
        (playing_cards.Rank.SIX, {6}),
        (playing_cards.Rank.SEVEN, {7}),
        (playing_cards.Rank.EIGHT, {8}),
        (playing_cards.Rank.NINE, {9}),
        (playing_cards.Rank.TEN, {10}),
        (playing_cards.Rank.JACK, {10}),
        (playing_cards.Rank.QUEEN, {10}),
        (playing_cards.Rank.KING, {10}),
    ],
)
def test__card__values(rank: playing_cards.Rank, values: set[int]):
    rank: playing_cards.Rank
    suit: playing_cards.Suit
    for suit in playing_cards.Suit:
        card = deck.Card(rank, suit)
        assert card.values == values


###
# Deck tests
###
def test__deck__can_be_reset():
    """
    Test that decks can be reset.
    """
    deck_ = deck.Deck(2)
    [deck_.take_card() for _ in range(10)]
    assert len(deck_) == 94

    deck_.reset()
    assert len(deck_) == 104
