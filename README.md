<span align="center">

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![tests](https://github.com/billwallis/blackjack/actions/workflows/tests.yaml/badge.svg)](https://github.com/billwallis/blackjack/actions/workflows/tests.yaml)
[![coverage](coverage.svg)](https://smarie.github.io/python-genbadge/)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/billwallis/blackjack/main.svg)](https://results.pre-commit.ci/latest/github/billwallis/blackjack/main)
![GitHub last commit](https://img.shields.io/github/last-commit/billwallis/blackjack)

</span>

---

# Blackjack ♠️♥️♣️♦️

Blackjack, also called 21.

## Sample Game 📝

Set up a game with some number of players and some number of decks:

```python
from blackjack.game import Game

game = Game(min_bet=10)
game.standard_setup(number_of_players=1, number_of_decks=6)
game.play_game()
```

A typical game will look something like this:

```
Dealer
[T♣ ??] [{10}]

Player_1 has £500 with hand:
    [3♥ 8♣] {11}  stake: £10


Player_1's turn:

Playing hand [3♥ 8♣] {11}
[h] Hit, [s] Stand, [d] Double down, [sp] Split?
Player chose DOUBLE_DOWN

Dealer [T♣ 3♣ 4♦] {17}


Player_1 [3♥ 8♣ Q♦] {21}
Outcome: win

Play another round? [Y/n]
--------------------

Game ended with:
  - Player_1: £510
```

## Contributing 🤝

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and then install the dependencies:

```bash
uvx --from poethepoet poe install
```
