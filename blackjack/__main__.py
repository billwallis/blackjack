from blackjack.game import GameControl


def main() -> None:
    # pass
    # deck = Deck(1)
    # print(deck)
    # [print(c) for c in deck.take_card(52)]
    # print(deck)

    # game = GameControl().standard_setup()
    # [print(p) for p in game.players]

    game = GameControl(num_players=1)
    game.play_round()


if __name__ == "__main__":
    main()
