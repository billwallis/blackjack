"""
Test the ``blackjack.participants`` module.
"""

import textwrap

import pytest

import blackjack
from blackjack import deck, participants


###
# Hand tests
###
def test__hand(
    mock_player: participants.Player,
    mock_hand: participants.Hand,
):
    """
    Test the construction of the ``Hand`` class.
    """
    assert mock_hand.bet == 10
    assert mock_hand.cards == []


def test__hand__str(mock_hand: participants.Hand):
    """
    Test the string representation of the ``Hand`` class.
    """
    assert str(mock_hand) == "[] {0}"
    mock_hand.cards = [
        deck.Card.from_id("2S"),
        deck.Card.from_id("TC"),
    ]
    assert str(mock_hand) == "[2♠ T♣] {12}"


def test__hand__len(mock_hand: participants.Hand):
    """
    Test the length of the ``Hand`` class.
    """
    assert len(mock_hand) == 0
    mock_hand.cards = [
        deck.Card.from_id("2S"),
        deck.Card.from_id("TC"),
    ]
    assert len(mock_hand) == 2


def test__hand__getitem(mock_hand: participants.Hand):
    """
    Test retrieving an item from the ``Hand`` class.
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
def test__hand__values(
    mock_hand: participants.Hand,
    cards: list[str],
    values: set[int],
    eligible_values: set[int],
):
    """
    Test the ``Hand.values``.
    """
    mock_hand.cards = [deck.Card.from_id(card) for card in cards]
    assert mock_hand.values == values


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
def test__hand__blackjack(
    mock_hand: participants.Hand,
    cards: list[str],
    expected: bool,
):
    """
    Test the ``Hand.blackjack`` property.
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
def test__hand__bust(
    mock_hand: participants.Hand,
    cards: list[str],
    expected: bool,
):
    """
    Test the ``Hand.bust`` property.
    """
    mock_hand.cards = [deck.Card.from_id(card) for card in cards]
    assert mock_hand.bust is expected


def test__hand__hit(mock_game: blackjack.Game, mock_hand: participants.Hand):
    """
    Test the ``Hand.hit()`` method.
    """
    assert len(mock_hand) == 0
    mock_hand.hit(mock_game.deck)
    assert len(mock_hand) == 1


@pytest.mark.parametrize(
    "cards",
    [
        (["AC"]),
        (["TC"]),
        (["TC", "AC"]),
        (["TC", "TD"]),
        (["AC", "AD"]),
        (["TC", "AC", "AD"]),
        (["TC", "TD", "2C"]),
    ],
)
def test__hand__hit__by_key(
    mock_game: blackjack.Game, mock_hand: participants.Hand, cards: list[str]
):
    """
    Test the ``Hand.hit()`` method with specific cards.
    """
    for card in cards:
        print(f"hitting for card {card}")
        mock_hand.hit(mock_game.deck, card)

    assert mock_hand.cards == [deck.Card.from_id(card) for card in cards]
    mock_hand.cards = []


def test__hand__deal(mock_game: blackjack.Game, mock_hand: participants.Hand):
    """
    Test the ``Hand.deal()`` method.
    """
    assert len(mock_hand) == 0
    mock_hand.deal(mock_game.deck)
    assert len(mock_hand) == 2


@pytest.mark.parametrize(
    "cards",
    [
        (["TC", "AC"]),
        (["TC", "TD"]),
        (["AC", "AD"]),
    ],
)
def test__hand__deal__by_keys(
    mock_game: blackjack.Game, mock_hand: participants.Hand, cards: list[str]
):
    """
    Test the ``Hand.deal()`` method with specific cards.
    """
    assert len(mock_hand) == 0
    mock_hand.deal(mock_game.deck, _keys=cards)
    assert len(mock_hand) == 2
    assert mock_hand.cards == [deck.Card.from_id(card) for card in cards]


def test__hand__deal__raises(
    mock_game: blackjack.Game, mock_hand: participants.Hand
):
    """
    Test that the ``Hand.deal()`` method raises an exception.
    """
    assert len(mock_hand) == 0
    mock_hand.deal(mock_game.deck)
    with pytest.raises(ValueError):
        mock_hand.deal(mock_game.deck)


def test__hand__show(
    mock_game: blackjack.Game,
    mock_hand: participants.Hand,
):
    """
    Test the ``Hand.show_cards()`` method.
    """
    assert len(mock_hand) == 0
    mock_hand.deal(mock_game.deck, ["TC", "AC"])
    shown_hand = mock_hand.show()
    assert shown_hand == "[T♣ A♣] {11, 21}"


###
# DealerHand tests
###
def test__dealer_hand():
    """
    Test the ``DealerHand.evaluate()`` method.
    """
    dealer_hand = participants.Hand(bet=None)
    assert len(dealer_hand) == 0

    dealer_hand.cards = [
        deck.Card.from_id("2C"),
        deck.Card.from_id("AC"),
    ]
    assert dealer_hand.show(masked=True) == "[2♣ ??] [{2}]\n"
    assert dealer_hand.show() == "[2♣ A♣] {3, 13}"


###
# PlayerHand tests
###
def test__player_hand():
    player_hand = participants.PlayerHand(bet=10)
    assert player_hand.cards == []
    assert player_hand.bet == 10
    assert player_hand.from_split is False
    assert player_hand.playing is True


def test__player_hand__split(
    mock_game: blackjack.Game,
    mock_player: participants.Player,
):
    """
    Test the ``PlayerHand.split()`` method.
    """
    mock_player.add_hand(bet=10)
    player_hand = mock_player.hands[0]
    player_hand.cards = [
        deck.Card.from_id("TC"),
        deck.Card.from_id("TD"),
    ]

    assert len(mock_player.hands) == 1
    player_hand.split(mock_game.deck, mock_player)
    assert len(mock_player.hands) == 2
    hand_0: participants.PlayerHand = mock_player.hands[0]
    hand_1: participants.PlayerHand = mock_player.hands[1]
    assert hand_1.bet == hand_0.bet

    assert len(hand_0) == 2
    assert hand_0.cards[0] == deck.Card.from_id("TC")
    assert hand_0.from_split is False
    assert hand_0.playing is True

    assert len(hand_1) == 2
    assert hand_1.cards[0] == deck.Card.from_id("TD")
    assert hand_1.from_split is True
    assert hand_1.playing is True


def test__player_hand__split__from_aces(
    mock_game: blackjack.Game,
    mock_player: participants.Player,
):
    """
    Test the ``PlayerHand.split()`` method on a pair of Aces.
    """
    mock_player.add_hand(bet=10)
    player_hand = mock_player.hands[0]
    player_hand.cards = [
        deck.Card.from_id("AC"),
        deck.Card.from_id("AD"),
    ]

    assert len(mock_player.hands) == 1
    player_hand.split(mock_game.deck, mock_player)
    assert len(mock_player.hands) == 2
    hand_0: participants.PlayerHand = mock_player.hands[0]
    hand_1: participants.PlayerHand = mock_player.hands[1]
    assert hand_1.bet == hand_0.bet

    assert len(hand_0) == 2
    assert hand_0.cards[0] == deck.Card.from_id("AC")
    assert hand_0.from_split is False
    assert hand_0.playing is False

    assert len(hand_1) == 2
    assert hand_1.cards[0] == deck.Card.from_id("AD")
    assert hand_1.from_split is True
    assert hand_1.playing is False


@pytest.mark.skip("Not implemented")
def test__player_hand__play_hand(mock_game: blackjack.Game):
    """
    Test the ``PlayerHand.play_hand()`` method.
    """
    pass


###
# PlayerOption tests
###


def test__player_option__readable():
    """
    Test the ``PlayerOption.readable`` property.
    """
    assert participants.PlayerOption.STAND.readable == "[s] Stand"
    assert participants.PlayerOption.HIT.readable == "[h] Hit"
    assert participants.PlayerOption.DOUBLE_DOWN.readable == "[d] Double down"
    assert participants.PlayerOption.SPLIT.readable == "[sp] Split"
    assert (
        participants.PlayerOption.TAKE_INSURANCE.readable
        == "[t] Take insurance"
    )


@pytest.mark.parametrize(
    "option, playing, hands, cards",
    [
        (participants.PlayerOption.STAND, False, 1, 2),
        (participants.PlayerOption.HIT, True, 1, 3),
        (participants.PlayerOption.DOUBLE_DOWN, False, 1, 3),
        (participants.PlayerOption.SPLIT, True, 2, 2),
        (participants.PlayerOption.TAKE_INSURANCE, False, 1, 2),
    ],
)
def test__player_option__action(  # noqa: PLR0913
    mock_game: blackjack.Game,
    mock_player: participants.Player,
    option: participants.PlayerOption,
    playing: str,
    hands: int,
    cards: int,
):
    """
    Test the ``PlayerOption.action()`` method.
    """
    mock_player.add_hand(bet=10)
    player_hand = mock_player.hands[0]
    player_hand.cards = [
        deck.Card.from_id("TC"),
        deck.Card.from_id("TD"),
    ]

    assert player_hand.playing is True
    assert len(mock_player.hands) == 1
    assert len(player_hand) == 2

    option.action(mock_player, player_hand, mock_game.deck)

    assert player_hand.playing is playing
    assert len(mock_player.hands) == hands
    assert len(player_hand) == cards


###
# Dealer tests
###


def test__dealer():
    """
    Test the ``Dealer`` class.
    """
    dealer = participants.Dealer()

    assert dealer.name == "Dealer"


def test__dealer__str():
    """
    Test the ``Dealer`` class.
    """
    dealer = participants.Dealer()

    assert str(dealer) == "Dealer"


###
# Player tests
###


def test__player(mock_game: blackjack.Game):
    """
    Test the ``Player`` class.
    """
    player = participants.Player(game=mock_game, name="Mock Player")

    assert player.name == "Mock Player"
    assert player.hands == []
    assert player.money == 500
    assert player.insurance == 0


def test__player__str__(mock_player: participants.Player):
    """
    Test the ``Player.__str__()`` method.
    """
    assert str(mock_player) == "Mock Player"


def test__player__len(mock_player: participants.Player):
    """
    Test the ``Player.__len__()`` method.
    """
    assert len(mock_player) == 0
    mock_player.add_hand(bet=10)
    assert len(mock_player) == 1
    mock_player.add_hand(bet=10)
    assert len(mock_player) == 2


def test__player__getitem(mock_player: participants.Player):
    """
    Test the ``Player.__getitem__()`` method.
    """
    mock_player.add_hand(bet=10)
    mock_player.add_hand(bet=10)

    assert mock_player[0] == mock_player.hands[0]
    assert mock_player[1] == mock_player.hands[1]


def test__player__add_hand(mock_player: participants.Player):
    """
    Test the ``Player.add_hand()`` method.
    """
    assert len(mock_player) == 0
    mock_player.add_hand(bet=10)
    assert len(mock_player) == 1
    mock_player.add_hand(bet=10)
    assert len(mock_player) == 2


def test__player__clear_hands(mock_player: participants.Player):
    """
    Test the ``Player.clear_hands()`` method.
    """
    mock_player.add_hand(bet=10)
    mock_player.add_hand(bet=10)

    assert len(mock_player) == 2
    mock_player.clear_hands()
    assert len(mock_player) == 0


def test__player__add_money(
    mock_player: participants.Player,
    capsys: pytest.CaptureFixture,
):
    """
    Test the ``Player.add_money()`` method.
    """
    mock_player.money = 500
    mock_player.add_money(100)
    captured = capsys.readouterr()

    assert mock_player.money == 600
    assert captured.out.strip() == "Mock Player won 100"


def test__player__print_money(
    mock_player: participants.Player,
    capsys: pytest.CaptureFixture,
):
    """
    Test the ``Player.print_money()`` method.
    """
    mock_player.money = 500
    mock_player.print_money()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Mock Player has 500 money"


def test__player__name_and_money(mock_player: participants.Player):
    """
    Test the ``Player.print_name_and_money()`` method.
    """
    mock_player.money = 500

    mock_player.add_hand(bet=10)
    mock_player.hands[0].cards = [
        deck.Card.from_id("TC"),
        deck.Card.from_id("TD"),
    ]
    assert len(mock_player.hands) == 1
    assert (
        mock_player.name_and_money.strip()
        == textwrap.dedent(
            """
        Mock Player has £500 with hand:
            [T♣ T♦] {20}  stake: £10
        """
        ).strip()
    )

    mock_player.add_hand(bet=10)
    mock_player.hands[1].cards = [
        deck.Card.from_id("AC"),
        deck.Card.from_id("AD"),
    ]
    assert len(mock_player.hands) == 2
    assert (
        mock_player.name_and_money.strip()
        == textwrap.dedent(
            """\
        Mock Player has £500 with hands:
            [T♣ T♦] {20}  stake: £10
            [A♣ A♦] {2, 12}  stake: £10
        """
        ).strip()
    )


# fmt: off
_opt = participants.PlayerOption  # For brevity
@pytest.mark.parametrize(
    "cards, options",
    [
        (["TC", "AC"], [_opt.TAKE_INSURANCE, _opt.STAND, _opt.HIT, _opt.DOUBLE_DOWN]),
        (["TC", "TD"], [_opt.STAND, _opt.HIT, _opt.DOUBLE_DOWN, _opt.SPLIT]),
        (["AC", "AD"], [_opt.STAND, _opt.HIT, _opt.DOUBLE_DOWN, _opt.SPLIT]),
        (["JC", "KD"], [_opt.STAND, _opt.HIT, _opt.DOUBLE_DOWN]),
        (["2C", "3D"], [_opt.STAND, _opt.HIT, _opt.DOUBLE_DOWN]),
        (["TC", "AC", "AD"], [_opt.STAND, _opt.HIT]),
        (["TC", "TD", "2C"], []),
    ],
)
def test__player_hand__options__dealer_has_ace(
    mock_game: blackjack.Game,
    mock_player: participants.Player,
    cards: list[str],
    options: list[participants.PlayerOption],
):
    """
    Test the ``PlayerHand.options`` property.

    TODO: Improve this with more cases (especially for dealer hands).
    """
    mock_game.dealer.hand.cards = [deck.Card.from_id("AS")]
    player_hand = participants.PlayerHand(bet=10)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]

    assert options == participants.get_options(mock_player, player_hand, mock_game)


def test__player_hand__options__dealer_no_ace(
    mock_game: blackjack.Game,
    mock_player: participants.Player,
):
    """
    Test the ``PlayerHand.options`` property.
    """
    cards, options = ["TC", "AC"], []
    mock_game.dealer.hand.cards = [deck.Card.from_id("TS")]
    player_hand = participants.PlayerHand(bet=10)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]

    assert options == participants.get_options(mock_player, player_hand, mock_game)
# fmt: on
