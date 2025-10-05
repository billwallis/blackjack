import pytest

from blackjack import deck, game, participants


@pytest.fixture
def mock_game() -> game.Game:
    """
    A game with six players and six decks.
    """
    game_ = game.Game(min_bet=10)
    game_.standard_setup(number_of_players=6, number_of_decks=6)

    return game_


@pytest.fixture
def dealer_with_17() -> participants.Dealer:
    """
    A dealer with a hand value of 17 (10 of Spades and 7 of Spades).
    """
    dealer = participants.Dealer()
    dealer.hand.cards = [
        deck.Card.from_id("TS"),
        deck.Card.from_id("7S"),
    ]
    return dealer


@pytest.fixture
def dealer_with_ace_first_blackjack() -> participants.Dealer:
    """
    A dealer with a hand value of 21 (Ace of Spades and 10 of Spades).
    """
    dealer = participants.Dealer()
    dealer.hand.cards = [
        deck.Card.from_id("AS"),
        deck.Card.from_id("TS"),
    ]
    return dealer


@pytest.fixture
def dealer_with_ten_first_blackjack() -> participants.Dealer:
    """
    A dealer with a hand value of 21 (10 of Spades and Ace of Spades).
    """
    dealer = participants.Dealer()
    dealer.hand.cards = [
        deck.Card.from_id("TS"),
        deck.Card.from_id("AS"),
    ]
    return dealer


@pytest.fixture
def dealer_with_bust() -> participants.Dealer:
    """
    A dealer with a bust hand (10 of Spades, 10 of Clubs, 2 of Diamonds).
    """
    dealer = participants.Dealer()
    dealer.hand.cards = [
        deck.Card.from_id("TS"),
        deck.Card.from_id("TC"),
        deck.Card.from_id("TD"),
    ]
    return dealer


@pytest.fixture
def mock_player() -> participants.Player:
    """
    A player.
    """
    return participants.Player("Mock Player", 500)


@pytest.fixture
def mock_hand() -> participants.Hand:
    """
    A hand with a bet of 10.
    """

    class MockHand(participants.Hand):
        def evaluate(self) -> None:
            pass  # pragma: no cover

    return MockHand(bet=10)
