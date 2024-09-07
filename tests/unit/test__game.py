"""
Test the ``blackjack.game`` module.
"""

import pytest

from blackjack import deck, game, participants


@pytest.mark.skip("Not implemented")
def test__player_hand_can_be_played(
    mock_game: game.Game,
    mock_player: participants.Player,
):
    """
    A player hand can be played.
    """
    game.play_hand(mock_player.hands[0], mock_game, mock_player)


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

    game.action(player_hand, option, mock_player, mock_game.deck)
    assert player_hand.playing is is_playing
    assert len(mock_player.hands) == number_of_hands
    assert len(player_hand) == number_of_cards


def test__game__can_be_initialised():
    """
    A game can be initialised.
    """
    game_ = game.Game(min_bet=10)

    assert pytest.raises(AttributeError, lambda: game_.deck)
    assert pytest.raises(AttributeError, lambda: game_.dealer)
    assert game_.players == []
    assert game_.min_bet == 10
    assert game_.round == 0
    assert str(game_) == "Game consisting of 0 players"

    game_.add_player("Player_1", 500)
    game_.add_player("Player_2", 500)
    assert str(game_) == "Game consisting of 2 players"


def test__game__standard_setup_adds_deck_dealer_and_players():
    """
    A standard setup adds a deck, a dealer, and a number of players to the
    game.
    """
    game_ = game.Game(min_bet=10)
    game_.standard_setup(number_of_players=6, number_of_decks=6)

    assert len(game_.deck) == 52 * 6
    assert type(game_.deck) is deck.Deck
    assert type(game_.dealer) is participants.Dealer
    assert all(type(player) is participants.Player for player in game_.players)


def test__game__cannot_add_deck_if_one_already_exists():
    """
    A deck cannot be added to the game if one already exists in the game.
    """
    game_ = game.Game(min_bet=10)
    game_.add_deck(1)
    assert pytest.raises(AssertionError, lambda: game_.add_deck(1))


def test__game__cannot_add_dealer_if_one_already_exists():
    """
    A dealer cannot be added to the game if one already exists in the game.
    """
    game_ = game.Game(min_bet=10)
    game_.add_dealer()
    assert pytest.raises(AssertionError, lambda: game_.add_dealer())


def test__game__cannot_add_a_player_with_an_existing_name():
    """
    A player cannot be added to the game if a player with the same name
    already exists in the game.
    """
    game_ = game.Game(min_bet=10)
    assert game_.players == []

    game_.add_player("Player_1", 100)
    assert len(game_.players) == 1
    assert type(game_.players[0]) is participants.Player
    assert game_.players[0].name == "Player_1"

    with pytest.raises(ValueError):
        game_.add_player("Player_1", 200)


@pytest.mark.skip(reason="Not implemented")
def test__game__round_can_be_played(mock_game: game.Game):
    """
    A round of Blackjack can be played.
    """
    mock_game.play_round()


def test__game__dealer_hand_can_be_evaluated():
    """
    The dealer's hand can be evaluated.
    """
    game_ = game.Game(min_bet=10)
    game_.add_deck(1)
    dealer = game_.add_dealer()
    assert len(dealer.hand) == 0

    dealer.hand.cards = [
        deck.Card.from_id("2C"),
        deck.Card.from_id("AC"),
    ]
    game_.evaluate_dealer()
    assert len(dealer.hand) >= 2
    assert max(dealer.hand.values) >= 17


@pytest.mark.parametrize(
    "cards, outcome",
    [
        (["TC", "AC"], participants.PlayerOutcome.WIN),
        (["TC", "TD"], participants.PlayerOutcome.WIN),
        (["TC", "7D"], participants.PlayerOutcome.DRAW),
        (["TC", "4D", "3D"], participants.PlayerOutcome.DRAW),
        (["AC", "AD"], participants.PlayerOutcome.LOSE),
        (["2C", "3D"], participants.PlayerOutcome.LOSE),
        (["TC", "AC", "AD"], participants.PlayerOutcome.LOSE),
        (["TC", "TD", "2C"], participants.PlayerOutcome.LOSE),
    ],
)
def test__game__player_hand_can_be_evaluated__dealer_with_17(
    mock_game: game.Game,
    mock_player: participants.Player,
    dealer_with_17: participants.Dealer,
    cards: list[str],
    outcome: participants.PlayerOutcome,
):
    """
    The player hand can be evaluated against a dealer with a hand value of 17.

    TODO: Improve this with more cases (especially for dealer hands).
    """
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]
    mock_game.dealer = dealer_with_17

    mock_game.evaluate_player(player_hand, mock_player)
    assert player_hand.outcome is outcome


@pytest.mark.parametrize(
    "cards, outcome",
    [
        (["TC", "AC"], participants.PlayerOutcome.WIN),
        (["TC", "TD"], participants.PlayerOutcome.WIN),
        (["TC", "9D"], participants.PlayerOutcome.WIN),
        (["TC", "4D", "5D"], participants.PlayerOutcome.WIN),
        (["AC", "AD"], participants.PlayerOutcome.WIN),
        (["2C", "3D"], participants.PlayerOutcome.WIN),
        (["TC", "AC", "AD"], participants.PlayerOutcome.WIN),
        (["TC", "TD", "2C"], participants.PlayerOutcome.LOSE),
    ],
)
def test__player_hand_can_be_evaluated__dealer_with_bust(
    mock_game: game.Game,
    mock_player: participants.Player,
    dealer_with_bust: participants.Dealer,
    cards: list[str],
    outcome: participants.PlayerOutcome,
):
    """
    The player hand can be evaluated against a dealer with a bust hand.

    TODO: Improve this with more cases (especially for dealer hands).
    """
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]
    mock_game.dealer = dealer_with_bust

    mock_game.evaluate_player(player_hand, mock_player)
    assert player_hand.outcome is outcome


@pytest.mark.parametrize(
    "cards, outcome",
    [
        (["TC", "AC"], participants.PlayerOutcome.DRAW),
        (["TC", "TD"], participants.PlayerOutcome.LOSE),
        (["TC", "9D"], participants.PlayerOutcome.LOSE),
        (["TC", "4D", "5D"], participants.PlayerOutcome.LOSE),
        (["AC", "AD"], participants.PlayerOutcome.LOSE),
        (["2C", "3D"], participants.PlayerOutcome.LOSE),
        (["TC", "AC", "AD"], participants.PlayerOutcome.LOSE),
        (["TC", "TD", "2C"], participants.PlayerOutcome.LOSE),
    ],
)
def test__player_hand_can_be_evaluated__dealer_with_ace_first_blackjack(
    mock_game: game.Game,
    mock_player: participants.Player,
    dealer_with_ace_first_blackjack: participants.Dealer,
    cards: list[str],
    outcome: participants.PlayerOutcome,
):
    """
    The player hand can be evaluated against a dealer with an Ace-first
    Blackjack.

    TODO: Improve this with more cases (especially for dealer hands).
    """
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]
    mock_game.dealer = dealer_with_ace_first_blackjack

    mock_game.evaluate_player(player_hand, mock_player)
    assert player_hand.outcome is outcome


@pytest.mark.parametrize(
    "cards, outcome",
    [
        (["TC", "AC"], participants.PlayerOutcome.DRAW),
        (["TC", "TD"], participants.PlayerOutcome.LOSE),
        (["TC", "9D"], participants.PlayerOutcome.LOSE),
        (["TC", "4D", "5D"], participants.PlayerOutcome.LOSE),
        (["AC", "AD"], participants.PlayerOutcome.LOSE),
        (["2C", "3D"], participants.PlayerOutcome.LOSE),
        (["TC", "AC", "AD"], participants.PlayerOutcome.LOSE),
        (["TC", "TD", "2C"], participants.PlayerOutcome.LOSE),
    ],
)
def test__player_hand_can_be_evaluated__dealer_with_ten_first_blackjack(
    mock_game: game.Game,
    mock_player: participants.Player,
    dealer_with_ten_first_blackjack: participants.Dealer,
    cards: list[str],
    outcome: participants.PlayerOutcome,
):
    """
    The player hand can be evaluated against a dealer with a Ten-first
    Blackjack.

    TODO: Improve this with more cases (especially for dealer hands).
    """
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]
    mock_game.dealer = dealer_with_ten_first_blackjack

    mock_game.evaluate_player(player_hand, mock_player)
    assert player_hand.outcome is outcome


def test__player_hand_can_be_evaluated__edge_cases(
    mock_game: game.Game,
    mock_player: participants.Player,
):
    """
    The player hand can be evaluated in edge cases.
    """
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    player_hand.cards = [
        deck.Card.from_id(card) for card in ["2H", "4C", "5D", "JH"]
    ]

    mock_game.dealer = participants.Dealer()
    mock_game.dealer.hand.cards = [
        deck.Card.from_id(card) for card in ["9D", "7H", "AS"]
    ]

    assert len(mock_game.dealer.hand.cards) == 3

    mock_game.evaluate_player(player_hand, mock_player)
    assert player_hand.outcome is participants.PlayerOutcome.WIN


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
def test__game__player_can_be_given_options__dealer_has_an_ace(
    mock_game: game.Game,
    mock_player: participants.Player,
    cards: list[str],
    options: list[participants.PlayerOption],
):
    """
    The player can be given options based on their hand and the dealer's hand
    when the dealer's face-up card is an Ace.

    TODO: Improve this with more cases (especially for dealer hands).
    """
    mock_game.dealer.hand.cards = [deck.Card.from_id("AS")]
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]

    assert options == mock_game.get_player_options(mock_player, player_hand)


def test__game__player_can_be_given_options__dealer_does_not_have_an_ace(
    mock_game: game.Game,
    mock_player: participants.Player,
):
    """
    The player can be given options based on their hand and the dealer's hand
    when the dealer's face-up card is not an Ace.
    """
    cards, options = ["TC", "AC"], []
    mock_game.dealer.hand.cards = [deck.Card.from_id("TS")]
    player_hand = participants.PlayerHand(bet=10, from_split=False)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]

    assert options == mock_game.get_player_options(mock_player, player_hand)
# fmt: on
