"""
Test the ``blackjack.game`` module.
"""

import pytest

from blackjack import deck, game, participants


@pytest.fixture(scope="function")
def mock_game() -> game.Game:
    """
    Create a mock ``Game`` instance.
    """
    return game.Game()


def test__game() -> None:
    """
    Test the construction of the ``Game`` class.
    """
    game_ = game.Game(min_bet=10)

    assert pytest.raises(AttributeError, lambda: game_.deck)
    assert pytest.raises(AttributeError, lambda: game_.dealer)
    assert game_.players == []
    assert game_.min_bet == 10
    assert game_.round == 0


def test__game__str(mock_game: game.Game) -> None:
    """
    Test the ``Game.__str__()`` method.
    """
    mock_game.players = []
    assert str(mock_game) == "Game consisting of 0 players"

    mock_game.add_player("Player_1")
    assert str(mock_game) == "Game consisting of 1 player"

    mock_game.add_player("Player_2")
    assert str(mock_game) == "Game consisting of 2 players"


def test__game__standard_setup(mock_game: game.Game):
    """
    Test the ``Game.standard_setup()`` method.
    """
    mock_game.standard_setup(num_players=6, num_decks=6)

    assert len(mock_game.deck) == 52 * 6
    assert type(mock_game.deck) is deck.Deck
    assert type(mock_game.dealer) is participants.Dealer
    assert all(
        type(player) is participants.Player for player in mock_game.players
    )


def test__game__add_deck(mock_game: game.Game):
    """
    Test the ``Game.add_deck()`` method.
    """
    assert pytest.raises(AttributeError, lambda: mock_game.deck)

    mock_game.add_deck(num_decks=6)
    assert len(mock_game.deck) == 52 * 6
    assert type(mock_game.deck) is deck.Deck


def test__game__add_dealer(mock_game: game.Game):
    """
    Test the ``Game.add_dealer()`` method.
    """
    assert pytest.raises(AttributeError, lambda: mock_game.dealer)

    mock_game.add_dealer()
    assert type(mock_game.dealer) is participants.Dealer


def test__game__add_player(mock_game: game.Game):
    """
    Test the ``Game.add_player()`` method.
    """
    assert mock_game.players == []

    mock_game.add_player("Player_1")
    assert len(mock_game.players) == 1
    assert type(mock_game.players[0]) is participants.Player
    assert mock_game.players[0].name == "Player_1"

    mock_game.add_player("Player_2")
    assert len(mock_game.players) == 2
    assert type(mock_game.players[1]) is participants.Player
    assert mock_game.players[1].name == "Player_2"


def test__game__add_player__raises(mock_game: game.Game):
    """
    Test the ``Game.add_player()`` method.
    """
    assert mock_game.players == []

    mock_game.add_player("Player_1")
    assert len(mock_game.players) == 1
    assert type(mock_game.players[0]) is participants.Player
    assert mock_game.players[0].name == "Player_1"

    with pytest.raises(ValueError):
        mock_game.add_player("Player_1")


@pytest.mark.skip(reason="Not implemented")
def test__game__play_round(mock_game: game.Game):
    """
    Test the ``Game.play_round()`` method.
    """
    pass


def test__dealer_hand__evaluate(mock_game: game.Game):
    """
    Test the ``DealerHand.evaluate()`` method.
    """
    mock_game.add_deck(1)
    dealer = mock_game.add_dealer()
    assert len(dealer.hand) == 0

    dealer.hand.cards = [
        deck.Card.from_id("2C"),
        deck.Card.from_id("AC"),
    ]
    mock_game.evaluate_dealer()
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
def test__player_hand__evaluate__dealer_with_17(
    mock_game: game.Game,
    mock_player: participants.Player,
    dealer_with_17: participants.Dealer,
    cards: list[str],
    outcome: participants.PlayerOutcome,
):
    """
    Test the ``PlayerHand.evaluate()`` method.

    TODO: Improve this with more cases (especially for dealer hands).
    """
    player_hand = participants.PlayerHand(bet=10)
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
def test__player_hand__evaluate__dealer_with_bust(
    mock_game: game.Game,
    mock_player: participants.Player,
    dealer_with_bust: participants.Dealer,
    cards: list[str],
    outcome: participants.PlayerOutcome,
):
    """
    Test the ``PlayerHand.evaluate()`` method.

    TODO: Improve this with more cases (especially for dealer hands).
    """
    player_hand = participants.PlayerHand(bet=10)
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
def test__player_hand__evaluate__dealer_with_ace_first_blackjack(
    mock_game: game.Game,
    mock_player: participants.Player,
    dealer_with_ace_first_blackjack: participants.Dealer,
    cards: list[str],
    outcome: participants.PlayerOutcome,
):
    """
    Test the ``PlayerHand.evaluate()`` method.

    TODO: Improve this with more cases (especially for dealer hands).
    """
    player_hand = participants.PlayerHand(bet=10)
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
def test__player_hand__evaluate__dealer_with_ten_first_blackjack(
    mock_game: game.Game,
    mock_player: participants.Player,
    dealer_with_ten_first_blackjack: participants.Dealer,
    cards: list[str],
    outcome: participants.PlayerOutcome,
):
    """
    Test the ``PlayerHand.evaluate()`` method.

    TODO: Improve this with more cases (especially for dealer hands).
    """
    player_hand = participants.PlayerHand(bet=10)
    player_hand.cards = [deck.Card.from_id(card) for card in cards]
    mock_game.dealer = dealer_with_ten_first_blackjack

    mock_game.evaluate_player(player_hand, mock_player)
    assert player_hand.outcome is outcome


def test__player_hand__evaluate__edge_cases(
    mock_game: game.Game,
    mock_player: participants.Player,
):
    """
    Test the ``PlayerHand.evaluate()`` method.
    """
    player_hand = participants.PlayerHand(bet=10)
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
