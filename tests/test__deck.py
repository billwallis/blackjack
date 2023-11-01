"""
Test the ``blackjack.deck`` module.
"""
import itertools

import pytest

from blackjack import deck


###
# Suit tests
###
@pytest.mark.parametrize(
    "suit_name",
    [
        "club",
        "spade",
        "heart",
        "diamond",
    ],
)
def test__suit(suit_name: str):
    """
    Test the construction of the ``Suit`` class.
    """
    suit = deck.Suit(suit_name)
    assert suit.name == suit_name.upper()
    assert suit.value == suit_name.lower()
    assert suit.id == suit_name[0].upper()
    assert str(suit) == suit_name
    assert repr(suit) == f"<Suit.{suit.name}: '{suit.value}'>"


@pytest.mark.parametrize(
    "suit_1, suit_2, expected",
    [
        (deck.Suit.CLUB, deck.Suit.CLUB, False),
        (deck.Suit.CLUB, deck.Suit.SPADE, True),
        (deck.Suit.CLUB, deck.Suit.HEART, True),
        (deck.Suit.CLUB, deck.Suit.DIAMOND, True),
        (deck.Suit.SPADE, deck.Suit.CLUB, False),
        (deck.Suit.HEART, deck.Suit.CLUB, False),
        (deck.Suit.DIAMOND, deck.Suit.CLUB, False),
    ],
)
def test__suit__lt(suit_1: deck.Suit, suit_2: deck.Suit, expected: bool):
    """
    Test the ``Suit.__lt__()`` method.
    """
    assert (suit_1 < suit_2) is expected


@pytest.mark.parametrize(
    "id_, suit",
    [
        ("C", deck.Suit.CLUB),
        ("S", deck.Suit.SPADE),
        ("H", deck.Suit.HEART),
        ("D", deck.Suit.DIAMOND),
    ],
)
def test__suit__from_id(id_: str, suit: deck.Suit):
    """
    Test the ``Suit.from_id()`` method.
    """
    assert deck.Suit.from_id(id_) == suit


def test__suit__from_id__raises():
    """
    Test that the ``Suit.from_id()`` method throws and exception.
    """
    with pytest.raises(KeyError):
        deck.Suit.from_id("X")


@pytest.mark.parametrize(
    "suit, image",
    [
        (deck.Suit.CLUB, "♣"),
        (deck.Suit.SPADE, "♠"),
        (deck.Suit.HEART, "♥"),
        (deck.Suit.DIAMOND, "♦"),
    ],
)
def test__suit__image(suit: deck.Suit, image: str):
    """
    Test the ``Suit.image`` attribute.
    """
    assert suit.image == image


@pytest.mark.parametrize(
    "suit, colour",
    [
        (deck.Suit.CLUB, "black"),
        (deck.Suit.SPADE, "black"),
        (deck.Suit.HEART, "red"),
        (deck.Suit.DIAMOND, "red"),
    ],
)
def test__suit__colour(suit: deck.Suit, colour: deck.Colour):
    """
    Test the ``Suit.colour`` attribute.
    """
    assert suit.colour == colour


###
# Rank tests
###
@pytest.mark.parametrize(
    "rank_value",
    range(1, 14),
)
def test__rank(rank_value: int):
    """
    Test the construction of the ``Rank`` class.
    """
    rank = deck.Rank(rank_value)
    assert rank.value == rank_value
    assert str(rank) == str(rank_value)
    assert repr(rank) == f"<Rank.{rank.name}: {rank.value}>"


@pytest.mark.parametrize(
    "id_, rank",
    [
        ("A", deck.Rank.ACE),
        ("2", deck.Rank.TWO),
        ("6", deck.Rank.SIX),
        ("T", deck.Rank.TEN),
        ("J", deck.Rank.JACK),
        ("Q", deck.Rank.QUEEN),
        ("K", deck.Rank.KING),
    ],
)
def test__rank__from_id(id_: str, rank: deck.Rank):
    assert deck.Rank.from_id(id_) == rank


@pytest.mark.parametrize(
    "rank, char",
    [
        (deck.Rank.ACE, "A"),
        (deck.Rank.TWO, "2"),
        (deck.Rank.THREE, "3"),
        (deck.Rank.FOUR, "4"),
        (deck.Rank.FIVE, "5"),
        (deck.Rank.SIX, "6"),
        (deck.Rank.SEVEN, "7"),
        (deck.Rank.EIGHT, "8"),
        (deck.Rank.NINE, "9"),
        (deck.Rank.TEN, "T"),
        (deck.Rank.JACK, "J"),
        (deck.Rank.QUEEN, "Q"),
        (deck.Rank.KING, "K"),
    ],
)
def test__rank__char(rank: deck.Rank, char: str):
    """
    Test the ``Rank.char`` attribute.
    """
    assert rank.id == char


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
def test__card():
    """
    Test the construction of the ``Card`` class.
    """
    for rank, suit in itertools.product(deck.Rank, deck.Suit):
        card = deck.Card(rank, suit)
        assert card.rank == rank
        assert card.suit == suit
        assert str(card) == rank.id + suit.id
        assert repr(card) == f"Card({rank=}, {suit=})"


@pytest.mark.parametrize(
    "card, other, result",
    [
        (deck.Card.from_str("2S"), deck.Card.from_str("TC"), {12}),
        (deck.Card.from_str("TC"), deck.Card.from_str("TC"), {20}),
        (deck.Card.from_str("2S"), 10, {12}),
        (deck.Card.from_str("TC"), 10, {20}),
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
        deck.Card.from_str("2S") + "2"  # type: ignore


def test__card__from_str():
    """
    Test the ``Card.from_str()`` method.
    """
    for rank, suit in itertools.product(deck.Rank, deck.Suit):
        card = deck.Card.from_str(rank.id + suit.id)
        assert card.rank == rank
        assert card.suit == suit


@pytest.mark.parametrize(
    "text, error",
    [
        ("A", KeyError),
        ("ABC", KeyError),
        ("S1", KeyError),
        ("B2", KeyError),
    ],
)
def test__card__from_str__raises(text: str, error: type[Exception]):
    """
    Test that the ``Card.from_str()`` method throws exceptions.
    """
    with pytest.raises(error):
        deck.Card.from_str(text)


@pytest.mark.parametrize(
    "rank, values",
    [
        (deck.Rank.ACE, {1, 11}),
        (deck.Rank.TWO, {2}),
        (deck.Rank.THREE, {3}),
        (deck.Rank.FOUR, {4}),
        (deck.Rank.FIVE, {5}),
        (deck.Rank.SIX, {6}),
        (deck.Rank.SEVEN, {7}),
        (deck.Rank.EIGHT, {8}),
        (deck.Rank.NINE, {9}),
        (deck.Rank.TEN, {10}),
        (deck.Rank.JACK, {10}),
        (deck.Rank.QUEEN, {10}),
        (deck.Rank.KING, {10}),
    ],
)
def test__card__values(rank: deck.Rank, values: set[int]):
    for suit in deck.Suit:
        card = deck.Card(rank, suit)  # type: ignore
        assert card.values == values


@pytest.mark.parametrize(
    "card, face",
    [
        (deck.Card(deck.Rank.ACE, deck.Suit.CLUB), "A♣"),
        (deck.Card(deck.Rank.TWO, deck.Suit.SPADE), "2♠"),
        (deck.Card(deck.Rank.TEN, deck.Suit.HEART), "T♥"),
        (deck.Card(deck.Rank.KING, deck.Suit.DIAMOND), "K♦"),
    ],
)
def test__card__face(card: deck.Card, face: str):
    assert card.face == face


@pytest.mark.parametrize(
    "card, colour",
    [
        (deck.Card(deck.Rank.ACE, deck.Suit.CLUB), "black"),
        (deck.Card(deck.Rank.TWO, deck.Suit.SPADE), "black"),
        (deck.Card(deck.Rank.TEN, deck.Suit.HEART), "red"),
        (deck.Card(deck.Rank.KING, deck.Suit.DIAMOND), "red"),
    ],
)
def test__colour(card: deck.Card, colour: deck.Colour):
    assert card.colour == colour


###
# Deck tests
###
def test__deck():
    """
    Test the construction of the ``Deck`` class.
    """
    deck_1 = deck.Deck()
    deck_2 = deck.Deck(num_decks=2)

    assert deck_1._num_decks == 1
    assert deck_2._num_decks == 2
    assert str(deck_1) == "Deck consisting of 52 cards"
    assert str(deck_2) == "Deck consisting of 104 cards"
    assert repr(deck_1) == f"Deck(num_decks={deck_1._num_decks})"
    assert repr(deck_2) == f"Deck(num_decks={deck_2._num_decks})"
    assert len(deck_1) == 52
    assert len(deck_2) == 104
    assert type(deck_1[0]) is deck.Card
    assert type(deck_2[0]) is deck.Card


def test__deck__take_card():
    """
    Test the ``Deck.take_card()`` method.
    """
    deck_ = deck.Deck()
    assert len(deck_) == 52
    card = deck_.take_card()
    assert len(deck_) == 51
    assert type(card) is deck.Card
    assert card not in deck_


@pytest.mark.parametrize(
    "key, card",
    [
        ("AC", deck.Card(deck.Rank.ACE, deck.Suit.CLUB)),
        ("2S", deck.Card(deck.Rank.TWO, deck.Suit.SPADE)),
        ("TH", deck.Card(deck.Rank.TEN, deck.Suit.HEART)),
        ("KD", deck.Card(deck.Rank.KING, deck.Suit.DIAMOND)),
    ],
)
def test__deck__take_card_by_key(key: str, card: deck.Card):
    """
    Test the ``Deck._take_card_by_key()`` method.
    """
    deck_ = deck.Deck()
    taken_card = deck_._take_card_by_key(key)
    assert len(deck_) == 51
    assert taken_card == card
    assert taken_card not in deck_


@pytest.mark.parametrize(
    "key, card",
    [
        ("AC", deck.Card(deck.Rank.ACE, deck.Suit.CLUB)),
        ("2S", deck.Card(deck.Rank.TWO, deck.Suit.SPADE)),
        ("TH", deck.Card(deck.Rank.TEN, deck.Suit.HEART)),
        ("KD", deck.Card(deck.Rank.KING, deck.Suit.DIAMOND)),
    ],
)
def test__deck__take_card_by_key__multiple_decks(key: str, card: deck.Card):
    """
    Test the ``Deck._take_card_by_key()`` method on multiple decks.
    """
    deck_ = deck.Deck(num_decks=3)
    taken_card_1 = deck_._take_card_by_key(key)
    taken_card_2 = deck_._take_card_by_key(key)
    taken_card_3 = deck_._take_card_by_key(key)
    assert len(deck_) == (52 * 3) - 3
    assert taken_card_1 == taken_card_2 == taken_card_3 == card
    assert taken_card_1 not in deck_
