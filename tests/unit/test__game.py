"""
Tests for the ``blackjack.game`` module.
"""

import pytest

from blackjack import deck, game, participants


def test__game__can_be_initialised():
    """
    A game can be initialised.
    """
    game_ = game.Game(min_bet=10)

    with pytest.raises(AttributeError):
        assert (
            game_.deck
        )  # `assert` is just to stop "statement has no effect" warning
    with pytest.raises(AttributeError):
        assert (
            game_.dealer
        )  # `assert` is just to stop "statement has no effect" warning

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

    with pytest.raises(AssertionError):
        game_.add_deck(1)


def test__game__cannot_add_dealer_if_one_already_exists():
    """
    A dealer cannot be added to the game if one already exists in the game.
    """
    game_ = game.Game(min_bet=10)
    game_.add_dealer()

    with pytest.raises(AssertionError):
        game_.add_dealer()


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
