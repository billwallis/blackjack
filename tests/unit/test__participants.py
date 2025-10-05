"""
Tests for the ``blackjack.participants`` module.
"""

import textwrap

import pytest

from blackjack import deck, game, participants
from blackjack.constants import Colours


def test__player_option__is_readable():
    """
    The player options can be human-readable.
    """
    assert participants.PlayerOption.STAND.readable == "[s] Stand"
    assert participants.PlayerOption.HIT.readable == "[h] Hit"
    assert participants.PlayerOption.DOUBLE_DOWN.readable == "[d] Double down"
    assert participants.PlayerOption.SPLIT.readable == "[sp] Split"
    assert (
        participants.PlayerOption.TAKE_INSURANCE.readable
        == "[t] Take insurance"
    )


def test__hand__can_be_initialised(
    mock_player: participants.Player,
    mock_hand: participants.Hand,
):
    """
    Hands can be initialised with a bet and no cards.
    """
    assert mock_hand.bet == 10
    assert mock_hand.cards == []
    assert str(mock_hand) == "[] {0}"


def test__hand__has_a_length(mock_hand: participants.Hand):
    """
    Hands can have their length checked.
    """
    assert len(mock_hand) == 0
    mock_hand.cards = [
        deck.Card.from_id("2S"),
        deck.Card.from_id("TC"),
    ]
    assert len(mock_hand) == 2


def test__hand__get_card_by_position(mock_hand: participants.Hand):
    """
    A card can be retrieved from a hand by its position.
    """
    mock_hand.cards = [
        deck.Card.from_id("2S"),
        deck.Card.from_id("TC"),
    ]
    assert mock_hand[0] == deck.Card.from_id("2S")
    assert mock_hand[1] == deck.Card.from_id("TC")


@pytest.mark.parametrize(
    "cards, values, eligible_values",
    [
        ([], {0}, {0}),
        (["2S", "TC"], {12}, {12}),
        (["TC", "AC"], {11, 21}, {11, 21}),
        (["TC", "TD", "2C"], {22}, set()),
        (["9D", "7H", "AS"], {17, 27}, set()),
    ],
)
def test__hand__has_values_and_eligible_values(
    mock_hand: participants.Hand,
    cards: list[str],
    values: set[int],
    eligible_values: set[int],
):
    """
    Hands have values and eligible values.
    """
    mock_hand.cards = [deck.Card.from_id(card) for card in cards]
    assert mock_hand.values == deck.Values(values)


@pytest.mark.parametrize(
    "cards, expected",
    [
        (["TC", "AC"], True),
        (["TC", "TD"], False),
        (["AC", "AD"], False),
        (["TC", "AC", "AD"], False),
        (["TC", "TD", "2C"], False),
    ],
)
def test__hand__can_tell_if_it_is_blackjack(
    mock_hand: participants.Hand,
    cards: list[str],
    expected: bool,
):
    """
    Hands can determine if they are a blackjack.
    """
    mock_hand.cards = [deck.Card.from_id(card) for card in cards]
    assert mock_hand.blackjack is expected


@pytest.mark.parametrize(
    "cards, expected",
    [
        (["TC", "AC"], False),
        (["TC", "TD"], False),
        (["AC", "AD"], False),
        (["TC", "AC", "AD"], False),
        (["TC", "TD", "2C"], True),
    ],
)
def test__hand__can_tell_if_it_is_bust(
    mock_hand: participants.Hand,
    cards: list[str],
    expected: bool,
):
    """
    Hands can determine if they are bust.
    """
    mock_hand.cards = [deck.Card.from_id(card) for card in cards]
    assert mock_hand.bust is expected


def test__hand__can_hit_the_deck(
    mock_game: game.Game,
    mock_hand: participants.Hand,
):
    """
    Hands can take a card from the deck (a "hit").
    """
    assert len(mock_hand) == 0
    mock_hand.hit(mock_game.deck)
    assert len(mock_hand) == 1
    mock_hand.hit(mock_game.deck)
    assert len(mock_hand) == 2

    mock_hand.cards = []
    mock_game.deck.reset()
    cards = ["TC", "TD", "2C"]
    for card in cards:
        mock_hand.hit(mock_game.deck, card)

    assert mock_hand.cards == [deck.Card.from_id(card) for card in cards]


def test__hand__can_be_dealt_to(
    mock_game: game.Game,
    mock_hand: participants.Hand,
):
    """
    Hands can be dealt to from the deck.
    """
    assert len(mock_hand) == 0
    mock_hand.deal(mock_game.deck)
    assert len(mock_hand) == 2

    mock_hand.cards = []
    mock_game.deck.reset()
    cards = ["AC", "AD"]
    mock_hand.deal(mock_game.deck, _keys=cards)

    assert len(mock_hand) == 2
    assert mock_hand.cards == [deck.Card.from_id(card) for card in cards]


def test__hand__cannot_be_dealt_to_if_it_has_cards_already(
    mock_game: game.Game,
    mock_hand: participants.Hand,
):
    """
    Hands cannot be dealt to if they already have cards.
    """
    assert len(mock_hand) == 0
    mock_hand.hit(mock_game.deck)
    with pytest.raises(ValueError):
        mock_hand.deal(mock_game.deck)


def test__hand__can_be_shown(
    mock_game: game.Game,
    mock_hand: participants.Hand,
):
    """
    Hands can be shown in full or with the second card masked with the
    eligible values.
    """
    assert len(mock_hand) == 0

    mock_hand.deal(mock_game.deck, ["TC", "AC"])
    ten_of_clubs = f"{Colours.BLUE}T♣{Colours.END}"
    ace_of_clubs = f"{Colours.BLUE}A♣{Colours.END}"
    assert mock_hand.show() == f"[{ten_of_clubs} {ace_of_clubs}] {{11, 21}}"
    assert mock_hand.show(masked=True) == f"[{ten_of_clubs} ??] [{{10}}]"

    mock_hand.hit(mock_game.deck, "AS")
    ace_of_spades = f"{Colours.BLUE}A♠{Colours.END}"
    assert (
        mock_hand.show()
        == f"[{ten_of_clubs} {ace_of_clubs} {ace_of_spades}] {{12}}"
    )


def test__player_hand__can_be_initialised():
    """
    Player hands can be initialised with a bet and no cards.
    """
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    assert player_hand.cards == []
    assert player_hand.bet == 10
    assert player_hand.playing is True
    assert player_hand.from_split is False
    assert player_hand.insurance == 0


def test__player_hand__can_split(
    mock_game: game.Game,
    mock_player: participants.Player,
):
    """
    A player hand can be split into two player hands.
    """
    player_hand = mock_player.add_hand(bet=10)
    player_hand.cards = [
        deck.Card.from_id("TC"),
        deck.Card.from_id("TD"),
    ]

    assert len(mock_player.hands) == 1

    player_hand.split(mock_game.deck, mock_player)
    assert len(mock_player.hands) == 2

    hand_0, hand_1 = mock_player.hands
    assert hand_1.bet == hand_0.bet

    assert len(hand_0) == 2
    assert hand_0.cards[0] == deck.Card.from_id("TC")
    assert hand_0.from_split is True
    assert hand_0.playing is True

    assert len(hand_1) == 2
    assert hand_1.cards[0] == deck.Card.from_id("TD")
    assert hand_1.from_split is True
    assert hand_1.playing is True


def test__player_hand__can_split_aces(
    mock_game: game.Game,
    mock_player: participants.Player,
):
    """
    A player hand with a pair of Aces can be split into two player hands,
    and exactly one card is dealt to each hand.
    """
    player_hand = mock_player.add_hand(bet=10)
    player_hand.cards = [
        deck.Card.from_id("AC"),
        deck.Card.from_id("AD"),
    ]

    assert len(mock_player.hands) == 1

    player_hand.split(mock_game.deck, mock_player)
    assert len(mock_player.hands) == 2

    hand_0, hand_1 = mock_player.hands
    assert hand_1.bet == hand_0.bet

    assert len(hand_0) == 2
    assert hand_0.cards[0] == deck.Card.from_id("AC")
    assert hand_0.from_split is True
    assert hand_0.playing is False

    assert len(hand_1) == 2
    assert hand_1.cards[0] == deck.Card.from_id("AD")
    assert hand_1.from_split is True
    assert hand_1.playing is False


def test__dealer__can_be_initialised():
    """
    A dealer can be initialised with a name and an empty hand.
    """
    dealer = participants.Dealer()

    assert dealer.name == "Dealer"
    assert str(dealer) == "Dealer"
    assert dealer.hand.cards == []
    assert dealer.hand.bet is None


def test__player__can_be_initialised():
    """
    A player can be initialised with a name and an empty list of hands.
    """
    player = participants.Player("Mock Player", 500)

    assert player.name == "Mock Player"
    assert player.money == 500
    assert player.hands == []
    assert str(player) == "Mock Player"


def test__player__can_add_hands(mock_player: participants.Player):
    """
    A player can add hands to their list of hands, and the "length" of the
    player is the number of hands they have.
    """
    assert len(mock_player) == 0

    hand_1 = mock_player.add_hand(bet=10)
    assert len(mock_player) == 1

    hand_2 = mock_player.add_hand(bet=10)
    assert len(mock_player) == 2

    assert mock_player.hands == [hand_1, hand_2]


def test__player__name_and_money_can_be_displayed(
    mock_player: participants.Player,
):
    """
    A player's name and money can be displayed.
    """
    mock_player.money = 500
    mock_player.add_hand(bet=10)
    mock_player.hands[0].cards = [
        deck.Card.from_id("TC"),
        deck.Card.from_id("TD"),
    ]
    ten_of_clubs = f"{Colours.BLUE}T♣{Colours.END}"
    ten_of_diamonds = f"{Colours.RED}T♦{Colours.END}"

    assert len(mock_player.hands) == 1
    assert (
        mock_player.name_and_money.strip()
        == textwrap.dedent(
            f"""
            Mock Player has £500 with hand:
                [{ten_of_clubs} {ten_of_diamonds}] {{20}}  stake: £10
            """
        ).strip()
    )

    mock_player.add_hand(bet=10)
    mock_player.hands[1].cards = [
        deck.Card.from_id("AC"),
        deck.Card.from_id("AD"),
    ]
    ace_of_clubs = f"{Colours.BLUE}A♣{Colours.END}"
    ace_of_diamonds = f"{Colours.RED}A♦{Colours.END}"

    assert len(mock_player.hands) == 2
    assert (
        mock_player.name_and_money.strip()
        == textwrap.dedent(
            f"""\
            Mock Player has £500 with hands:
                [{ten_of_clubs} {ten_of_diamonds}] {{20}}  stake: £10
                [{ace_of_clubs} {ace_of_diamonds}] {{2, 12}}  stake: £10
            """
        ).strip()
    )
