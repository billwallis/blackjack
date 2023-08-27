"""
This script defines the classes
    * Card
    * MultiDeck
        * Deck(MultiDeck)

The MultiDeck is a collection of n Decks, and the Deck is a collection of 52 Cards.
The Cards represent the playing cards from the French-suited, standard 52-card pack.
There are currently no Joker cards in the Card class.

Dependencies
    * `random`
"""


import itertools
import random

# model-level constants
FACES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
SUITS = ["C", "D", "H", "S"]
SUITS_IMG = ["♠", "♥", "♣", "♦"]
SUITS_TEXT = ["Club", "Diamond", "Heart", "Spade"]

###
# consider including jokers in the future (not suited, but one red and one black)
###


class Card:
    """
    A class to represent a playing card from the French-suited, standard 52-card pack

    ...

    Properties
    ----------
    rank : int
        the integer between 1 and 13 corresponding to the rank of the card
    suit : str
        the string character corresponding to the first letter of the card's suit
    value : int
        the rank of the card capped at 10
    face : str
        the string character corresponding the the character on the card
    suit_full : str
        the full name of the cards suit
    colour : int
        the colour of the card with 0 corresponding to red and 1 corresponding to black
    colour_text : str
        the colour of the card
    key : str
        the 2-character string corresponding to face and suit, e.g. 2C

    Class Methods
    -------
    from_key(key)
        construct the instance using the 2-character string corresponding to face and suit

    """

    def __init__(self, rank: int, suit: str):
        """
        Parameters
            * rank -- an integer between 1 and 13
            * suit -- a string character from the list ['C', 'D', 'H', 'S']
        """
        if rank in range(1, 14):
            self.rank = rank
        else:
            raise ValueError(f"Bad rank argument passed: {rank}")
        if suit in SUITS:
            self.suit = suit
        else:
            raise ValueError(f"Bad suit argument passed: {suit}")

    def __repr__(self):
        return f"Card(rank={self.rank}, suit={self.suit})"

    def __str__(self):
        return self.key

    @property
    def value(self) -> int:
        return min(self.rank, 10)

    @property
    def face(self) -> str:
        return FACES[self.rank - 1]

    @property
    def suit_full(self) -> str:
        return SUITS_TEXT[SUITS.index(self.suit)]

    @property
    def colour(self) -> int:
        return int(self.suit in ["C", "S"])

    @property
    def colour_text(self) -> str:
        return ["red", "black"][self.colour]

    @property
    def key(self) -> str:
        return self.face + self.suit

    @classmethod
    def from_key(cls, key: str):
        rank = FACES.index(key[0]) + 1
        return cls(rank, key[1])


class MultiDeck:
    """
    A class to represent a multiple sets of 52-card French-suited deck that may or may not have all cards in them

    ...

    Properties
    ----------
    card_count : int
        the number of cards currently in the deck

    Methods
    -------
    reset
        clear the deck of all cards and rebuild it with all 52, then shuffle
    shuffle
        shuffle the deck
    take_card(amount) -> list
        take the 'top {amount}' cards from the deck and return them as a list
    take_card_by_key(key) -> list
        pop the card from the deck whose key corresponds to the passed key
        IndexError if the card has already been removed from the deck

    """

    def __init__(self, num_decks: int = 1, init_empty: bool = False):
        """
        Parameters
            * num_decks -- the number of 52-card decks to include in the multi-deck
            * init_empty -- bool to indicate whether the deck should be instantiated without cards
        """
        self.num_decks = num_decks
        self.cards = []
        if not init_empty:
            self.reset()

    def __str__(self):
        return f'Deck consisting of {self.card_count} card{["s", ""][self.card_count == 1]}'

    def __len__(self):
        return self.card_count

    def __setitem__(self, position):
        return self.cards[position]

    def __getitem__(self, position):
        return self.cards[position]

    @property
    def card_count(self) -> int:
        return len(self.cards)

    def reset(self):
        self.cards = [
            Card(1 + rank, suit)
            for _, suit, rank in itertools.product(
                range(self.num_decks), SUITS, range(13)
            )
        ]

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def take_card(self, amount: int) -> list:
        return [self.cards.pop() for _ in range(amount)]

    def take_card_by_key(self, key: str) -> list:
        index = 0
        for card in self.cards:
            if card.key == key:
                break
            index += 1
        return [self.cards.pop(index)]


# class Deck(MultiDeck):
#     """
#     Inherits MultiCard for the specific case where there is 1 deck
#     """
#     def __init__(self, init_empty: bool = False):
#         super().__init__(1, init_empty)
