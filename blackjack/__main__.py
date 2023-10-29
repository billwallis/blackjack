"""
Start a game of Blackjack.
"""
import blackjack


def main() -> None:
    """
    Start a game of Blackjack.
    """
    game = blackjack.Game()
    game.standard_setup(num_players=1, num_decks=6)
    game.play_round()


if __name__ == "__main__":
    main()
