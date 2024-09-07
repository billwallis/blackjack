"""
Start a game of Blackjack.
"""

import blackjack


def main() -> None:
    """
    Start a game of Blackjack.
    """
    game = blackjack.Game(min_bet=10)
    game.standard_setup(number_of_players=1, number_of_decks=6)

    playing = True
    while playing:
        game.play_round()
        play_again = input("\nPlay another round? [Y/n] ")
        playing = play_again.lower() in {"y", "yes", ""}
        game.reset_round()

    print("\nGame ended with:")
    for player in game.players:
        print(f"  - {player.name}: £{player.money}")


if __name__ == "__main__":
    main()
