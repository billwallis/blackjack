import pytest

import blackjack


@pytest.fixture
def mock_game() -> blackjack.Game:
    """
    Create a mock ``Game`` instance.
    """
    game_ = blackjack.Game()
    game_.standard_setup(num_players=6, num_decks=6)

    return game_
