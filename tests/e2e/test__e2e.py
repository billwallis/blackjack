"""
End-to-end tests for the Blackjack game.
"""

import random
import runpy

import pytest

from blackjack import game as game_
from blackjack import participants

pytestmark = pytest.mark.e2e


def random_option(_) -> str:
    """
    Return a random player option.
    """
    return random.choice(list(participants.PlayerOption)).value  # noqa: S311


def test__rounds_can_be_played(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    The rounds can be played to completion without any errors.
    """
    monkeypatch.setattr("builtins.input", random_option)

    for i in range(1000):
        print(f"\n--- Game {i + 1} ---\n")
        game = game_.Game(min_bet=10)
        game.standard_setup(number_of_players=3, number_of_decks=6)
        game.play_round()
        print(20 * "-")


def test__package_can_be_invoked(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    The package can be invoked from the command line.
    """
    # TODO: This mocks _every_ input, but some ask different questions
    monkeypatch.setattr("builtins.input", random_option)
    runpy.run_module("blackjack", run_name="__main__")
