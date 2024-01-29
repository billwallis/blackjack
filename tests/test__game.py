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
    assert all(type(player) is participants.Player for player in mock_game.players)


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


@pytest.mark.skip(reason="Not implemented")
def test__game__play_round(mock_game: game.Game):
    """
    Test the ``Game.play_round()`` method.
    """
    pass
