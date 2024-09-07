"""
Test the ``blackjack.deck`` module.
"""

import playing_cards
import pytest

from blackjack import deck


def test__values__can_be_initialised():
    """
    Values can be initialised with a set of integers.
    """
    value = deck.Values({1, 11})
    assert value._values == {1, 11}
    assert str(value) == "{1, 11}"
    assert repr(value) == f"Value(value={value._values})"


def test__values__can_be_compared_for_equality():
    """
    Values can be compared for equality.
    """
    value_1 = deck.Values({1})
    value_2 = deck.Values({1})
    assert value_1 == value_2
    assert (value_1 == "one") is False


@pytest.mark.parametrize(
    "set_1, set_2, expected",
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
def test__values__can_be_compared_as_a_total_order(
    set_1: set[int],
    set_2: set[int],
    expected: bool,
):
    """
    Values can be compared as a total order.
    """
    value_1 = deck.Values(set_1)
    value_2 = deck.Values(set_2)
    assert (value_1 < value_2) is expected
    assert (value_1 <= value_2) is expected
    assert (value_1 > value_2) is not expected
    assert (value_1 >= value_2) is not expected


@pytest.mark.parametrize(
    "set_1, set_2, result",
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
def test__values__can_be_added_together(
    set_1: set[int],
    set_2: set[int],
    result: set[int],
):
    """
    Values can be added together.
    """
    value_1 = deck.Values(set_1)
    value_2 = deck.Values(set_2)
    expected = deck.Values(result)

    assert value_1 + value_2 == expected
    assert value_2 + value_1 == expected


def test__values__cannot_be_added_to_non_numerics():
    """
    Values cannot be added to non-numerics.
    """
    with pytest.raises(TypeError):
        deck.Values({1}) + "1"  # type: ignore


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
def test__values__has_eligible_values(
    values: set[int],
    eligible_values: set[int],
):
    """
    The eligible values are the values that are lower than or equal to the
    blackjack value.
    """
    assert deck.Values(values).eligible_values == deck.Values(eligible_values)


@pytest.mark.parametrize(
    "card, other, result",
    [
        (deck.Card.from_id("2S"), deck.Card.from_id("TC"), {12}),
        (deck.Card.from_id("TC"), deck.Card.from_id("TC"), {20}),
        (deck.Card.from_id("2S"), 10, {12}),
        (deck.Card.from_id("TC"), 10, {20}),
    ],
)
def test__card__can_be_added_to_cards_and_ints(
    card: deck.Card, other: int | deck.Card, result: set[int]
):
    """
    Cards can be added to cards and integers.
    """
    expected = deck.Values(result)
    assert card + other == expected
    assert other + card == expected


def test__card__cannot_be_added_to_non_numerics():
    """
    Cards cannot be added to non-numerics.
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
def test__card__has_values(rank: playing_cards.Rank, values: set[int]):
    """
    Cards have values based on their rank.
    """
    rank: playing_cards.Rank
    suit: playing_cards.Suit
    expected = deck.Values(values)
    for suit in playing_cards.Suit:
        card = deck.Card(rank, suit)
        assert card.values == expected


def test__deck__can_be_reset():
    """
    Test that decks can be reset.
    """
    deck_ = deck.Deck(2)
    [deck_.take_card() for _ in range(10)]
    assert len(deck_) == 94

    deck_.reset()
    assert len(deck_) == 104
