<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![tests](https://github.com/billwallis/blackjack/actions/workflows/tests.yaml/badge.svg)](https://github.com/billwallis/blackjack/actions/workflows/tests.yaml)
[![coverage](coverage.svg)](https://github.com/dbrgn/coverage-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/billwallis/blackjack)

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/billwallis/blackjack/main.svg)](https://results.pre-commit.ci/latest/github/billwallis/blackjack/main)

</div>

---

# Blackjack ♠️♥️♣️♦️

Blackjack, also called 21.

## Sample Game 📝

Set up a game with some number of players and some number of decks:

```python
import blackjack

game = blackjack.Game(min_bet=10)
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

This is just a personal project (so this instruction is just for me).

```bash
pip install -r requirements.txt
pre-commit install --install-hooks
```
