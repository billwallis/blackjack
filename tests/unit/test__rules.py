"""
Tests for the ``blackjack.rules`` module.
"""

import pytest

from blackjack import deck, game, participants, rules

# Aliases for brevity
HIT = participants.PlayerOption.HIT
STAND = participants.PlayerOption.STAND
DOUBLE_DOWN = participants.PlayerOption.DOUBLE_DOWN
SPLIT = participants.PlayerOption.SPLIT
TAKE_INSURANCE = participants.PlayerOption.TAKE_INSURANCE


def test__dealer_hand_can_be_played():
    """
    The dealer's hand can be played.
    """
    game_ = game.Game(min_bet=10)
    game_.add_deck(1)
    dealer = game_.add_dealer()
    assert len(dealer.hand) == 0

    dealer.hand.cards = [
        deck.Card.from_id("2C"),
        deck.Card.from_id("AC"),
    ]
    rules.play_hand__dealer(dealer.hand, game_.deck)
    assert len(dealer.hand) >= 2
    assert max(dealer.hand.values) >= 17


@pytest.mark.skip("Not implemented")
def test__player_hand_can_be_played(
    mock_game: game.Game,
    mock_player: participants.Player,
):
    """
    A player hand can be played.
    """
    rules.play_hand__player(
        mock_player.hands[0],
        mock_game.dealer.hand,
        mock_player,
        mock_game.deck,
    )


@pytest.mark.parametrize(
    "option, is_playing, number_of_hands, number_of_cards",
    [
        (participants.PlayerOption.STAND, False, 1, 2),
        (participants.PlayerOption.HIT, True, 1, 3),
        (participants.PlayerOption.DOUBLE_DOWN, False, 1, 3),
        (participants.PlayerOption.SPLIT, True, 2, 2),
        (participants.PlayerOption.TAKE_INSURANCE, False, 1, 2),
    ],
)
def test__player_hand_can_take_an_action(
    mock_game: game.Game,
    mock_player: participants.Player,
    option: participants.PlayerOption,
    is_playing: bool,
    number_of_hands: int,
    number_of_cards: int,
):
    """
    A player hand can take an action and its state will change accordingly.
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

    rules.action(player_hand, option, mock_player, mock_game.deck)
    assert player_hand.playing is is_playing
    assert len(mock_player.hands) == number_of_hands
    assert len(player_hand) == number_of_cards


@pytest.mark.parametrize(
    "dealer_has_ace, cards, options",
    [
        # Dealer has an Ace
        (True, ["TC", "AC"], [HIT, STAND, DOUBLE_DOWN, TAKE_INSURANCE]),
        (True, ["TC", "TD"], [HIT, STAND, DOUBLE_DOWN, SPLIT, TAKE_INSURANCE]),
        (True, ["AC", "AD"], [HIT, STAND, DOUBLE_DOWN, SPLIT, TAKE_INSURANCE]),
        (True, ["JC", "KD"], [HIT, STAND, DOUBLE_DOWN, TAKE_INSURANCE]),
        (True, ["2C", "3D"], [HIT, STAND, DOUBLE_DOWN, TAKE_INSURANCE]),
        (True, ["TC", "AC", "AD"], [HIT, STAND]),
        (True, ["TC", "TD", "2C"], []),
        # Dealer does not have an Ace
        (False, ["TC", "AC"], []),
        (False, ["TC", "TD"], [HIT, STAND, DOUBLE_DOWN, SPLIT]),
        (False, ["AC", "AD"], [HIT, STAND, DOUBLE_DOWN, SPLIT]),
        (False, ["JC", "KD"], [HIT, STAND, DOUBLE_DOWN]),
        (False, ["2C", "3D"], [HIT, STAND, DOUBLE_DOWN]),
        (False, ["TC", "AC", "AD"], [HIT, STAND]),
        (False, ["TC", "TD", "2C"], []),
    ],
)
def test__player_hand_can_be_given_options(
    mock_player: participants.Player,
    dealer_has_ace: bool,
    cards: list[str],
    options: list[participants.PlayerOption],
):
    """
    The player can be given options based on their hand and the dealer's hand
    when the dealer's face-up card is an Ace.

    TODO: Improve this with more cases that test the player's money.
    """
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]

    assert options == rules.get_options_for_player_hand(
        mock_player,
        player_hand,
        dealer_has_ace,
    )


# fmt: off
@pytest.mark.parametrize(
    "dealer, cards, outcome",
    [
        # Dealer with 17
        ("dealer_with_17", ["TC", "AC"], participants.HandOutcome.WIN),
        ("dealer_with_17", ["TC", "TD"], participants.HandOutcome.WIN),
        ("dealer_with_17", ["TC", "7D"], participants.HandOutcome.DRAW),
        ("dealer_with_17", ["TC", "4D", "3D"], participants.HandOutcome.DRAW),
        ("dealer_with_17", ["AC", "AD"], participants.HandOutcome.LOSE),
        ("dealer_with_17", ["2C", "3D"], participants.HandOutcome.LOSE),
        ("dealer_with_17", ["TC", "AC", "AD"], participants.HandOutcome.LOSE),
        ("dealer_with_17", ["TC", "TD", "2C"], participants.HandOutcome.LOSE),

        # Dealer with bust
        ("dealer_with_bust", ["TC", "AC"], participants.HandOutcome.WIN),
        ("dealer_with_bust", ["TC", "TD"], participants.HandOutcome.WIN),
        ("dealer_with_bust", ["TC", "9D"], participants.HandOutcome.WIN),
        ("dealer_with_bust", ["TC", "4D", "5D"], participants.HandOutcome.WIN),
        ("dealer_with_bust", ["AC", "AD"], participants.HandOutcome.WIN),
        ("dealer_with_bust", ["2C", "3D"], participants.HandOutcome.WIN),
        ("dealer_with_bust", ["TC", "AC", "AD"], participants.HandOutcome.WIN),
        ("dealer_with_bust", ["TC", "TD", "2C"], participants.HandOutcome.LOSE),

        # Dealer with Ace-first Blackjack
        ("dealer_with_ace_first_blackjack", ["TC", "AC"], participants.HandOutcome.DRAW),
        ("dealer_with_ace_first_blackjack", ["TC", "TD"], participants.HandOutcome.LOSE),
        ("dealer_with_ace_first_blackjack", ["TC", "9D"], participants.HandOutcome.LOSE),
        ("dealer_with_ace_first_blackjack", ["TC", "4D", "5D"], participants.HandOutcome.LOSE),
        ("dealer_with_ace_first_blackjack", ["AC", "AD"], participants.HandOutcome.LOSE),
        ("dealer_with_ace_first_blackjack", ["2C", "3D"], participants.HandOutcome.LOSE),
        ("dealer_with_ace_first_blackjack", ["TC", "AC", "AD"], participants.HandOutcome.LOSE),
        ("dealer_with_ace_first_blackjack", ["TC", "TD", "2C"], participants.HandOutcome.LOSE),

        # Dealer with ten-first Blackjack
        ("dealer_with_ten_first_blackjack", ["TC", "AC"], participants.HandOutcome.DRAW),
        ("dealer_with_ten_first_blackjack", ["TC", "TD"], participants.HandOutcome.LOSE),
        ("dealer_with_ten_first_blackjack", ["TC", "9D"], participants.HandOutcome.LOSE),
        ("dealer_with_ten_first_blackjack", ["TC", "4D", "5D"], participants.HandOutcome.LOSE),
        ("dealer_with_ten_first_blackjack", ["AC", "AD"], participants.HandOutcome.LOSE),
        ("dealer_with_ten_first_blackjack", ["2C", "3D"], participants.HandOutcome.LOSE),
        ("dealer_with_ten_first_blackjack", ["TC", "AC", "AD"], participants.HandOutcome.LOSE),
        ("dealer_with_ten_first_blackjack", ["TC", "TD", "2C"], participants.HandOutcome.LOSE),
    ],
)
# fmt: on
def test__player_hand_can_be_evaluated(
    dealer: str,
    cards: list[str],
    outcome: participants.HandOutcome,
    request: pytest.FixtureRequest,
):
    """
    The player hand can be evaluated against a dealer.
    """
    dealer_hand = request.getfixturevalue(dealer).hand
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]

    assert outcome == rules.get_hand_outcome(player_hand, dealer_hand)


# fmt: off
@pytest.mark.parametrize(
    "dealer_cards, player_cards, outcome",
    [
        (["9D", "7H", "AS"], ["2H", "4C", "5D", "JH"], participants.HandOutcome.WIN),
    ],
)
# fmt: on
def test__player_hand_can_be_evaluated__edge_cases(
    dealer_cards: list[str],
    player_cards: list[str],
    outcome: participants.HandOutcome,
):
    """
    The player hand can be evaluated against a dealer for some edge cases.
    """
    dealer = participants.Dealer()
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    dealer.hand.cards = [deck.Card.from_id(card) for card in dealer_cards]
    player_hand.cards = [deck.Card.from_id(card) for card in player_cards]

    assert rules.get_hand_outcome(player_hand, dealer.hand) == outcome


def test__player_hand_can_have_outcome_applied():
    """
    The player hand can have an outcome applied to it.
    """
    player = participants.Player("Player_1", 500)
    player.add_hand(bet=10)
    player_hand = player.hands[0]
    player_hand.cards = [
        deck.Card.from_id("TC"),
        deck.Card.from_id("TD"),
    ]
    assert player.money == 500
    assert player_hand.bet == 10

    rules.apply_outcome(player, participants.HandOutcome.WIN, player_hand.bet)
    assert player.money == 510

    rules.apply_outcome(player, participants.HandOutcome.DRAW, player_hand.bet)
    assert player.money == 510

    rules.apply_outcome(player, participants.HandOutcome.LOSE, 100)
    assert player.money == 410
