"""
Start a game of Blackjack.
"""

from blackjack.game import Game


def main() -> None:
    """
    Start a game of Blackjack.
    """
    game = Game(min_bet=10)
    game.standard_setup(number_of_players=1, number_of_decks=6)
    game.play_game()


if __name__ == "__main__":
    main()
