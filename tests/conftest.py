import pytest

import blackjack
from blackjack import deck, participants


@pytest.fixture
def mock_game() -> blackjack.Game:
    """
    Create a mock ``Game`` instance.
    """
    game_ = blackjack.Game()
    game_.standard_setup(num_players=6, num_decks=6)

    return game_


@pytest.fixture
def dealer_with_17() -> participants.Dealer:
    dealer = participants.Dealer()
    dealer.hand.cards = [
        deck.Card.from_id("TS"),
        deck.Card.from_id("7S"),
    ]
    return dealer


@pytest.fixture
def dealer_with_ace_first_blackjack() -> participants.Dealer:
    dealer = participants.Dealer()
    dealer.hand.cards = [
        deck.Card.from_id("AS"),
        deck.Card.from_id("TS"),
    ]
    return dealer


@pytest.fixture
def dealer_with_ten_first_blackjack() -> participants.Dealer:
    dealer = participants.Dealer()
    dealer.hand.cards = [
        deck.Card.from_id("TS"),
        deck.Card.from_id("AS"),
    ]
    return dealer


@pytest.fixture
def dealer_with_bust() -> participants.Dealer:
    dealer = participants.Dealer()
    dealer.hand.cards = [
        deck.Card.from_id("TS"),
        deck.Card.from_id("TC"),
        deck.Card.from_id("TD"),
    ]
    return dealer


@pytest.fixture(scope="function")
def mock_player(mock_game: blackjack.Game) -> participants.Player:
    """
    Create a mock ``Player`` instance.
    """
    return participants.Player(game=mock_game, name="Mock Player")


class MockHand(participants.Hand):
    def evaluate(self) -> None:
        pass


@pytest.fixture(scope="function")
def mock_hand() -> participants.Hand:
    """
    Create a mock ``Hand`` instance.
    """
    return MockHand(bet=10)
