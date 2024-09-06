"""
End-to-end tests for the Blackjack game.
"""

import pytest

from blackjack import Game


@pytest.mark.e2e
def test__end_to_end(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test the end-to-end functionality of the Blackjack game.
    """
    # monkeypatch the "input" function so that the "player" chooses to
    # "stand" on every turn.
    #
    # - https://stackoverflow.com/a/36377194/8213085
    monkeypatch.setattr("builtins.input", lambda _: "s")

    for i in range(1000):
        print(f"\n--- Game {i} ---\n")
        game = Game()
        game.standard_setup(num_players=3, num_decks=6)
        game.play_round()
        print(20 * "-")
