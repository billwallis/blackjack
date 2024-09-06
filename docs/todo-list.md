# To Do List

## Base Game

- Implement cards 'burns' to keep some info hidden from the players
- Find out whether dealer blackjack beats player blackjack
- Find out whether a dealer blackjack beats a player 21
- Find out whether a player blackjack beats a dealer 21
- Split Aces should only get a single card each
- Include insurance for when dealer starts with A
- Add side bets!

## Nice UX

- Implement the game in pygame (partially for fun, partially to confirm that everything works correctly)

## Automated Strategy

- Simulate n plays (in x games?) using the strategy matrices
- Research common top strategies to give multiple matrices
- For each matrix, compute an expected return to player

## Card Counting

- Implement card counting per game to determine strategy

## Cards In Play

- Use all cards in play to determine strategy

## Odd results

Why did this count as a loss?

```
Dealer
[9D ??] [{9}]

Player_0 has £500 with hand:
    [2H 4C] {6}  stake: £10

Playing hand [2H 4C] {6}
[s] Stand, [h] Hit, [d] Double down? h
Playing hand [2H 4C 5D] {11}
[s] Stand, [h] Hit? h
Playing hand [2H 4C 5D JH] {21}
[s] Stand, [h] Hit? s
Dealer's hand:    [9D 7H AS] {17}
Player_0's hand:    [2H 4C 5D JH] {21}
Outcome: lose
```
