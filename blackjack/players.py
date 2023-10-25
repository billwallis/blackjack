"""
This script defines the classes
    * Dealer
    * Player
    * Hand

The classes...

Dependencies
    *
"""


class Hand:
    """
    A class to represent the hands (House and player) in Blackjack

    ...

    Properties
    ----------
    name: string
        Distinguish 'players' by name
    game: Game (check this)
        The current game in play
    verbose: bool (consider removing)
        Print to the console. Inherited from `game`
    deck: Deck (consider removing)
        The deck to take cards from. Inherited from `game`
    hand: list
        The collection of Cards that the House has
    value: list
        The list-value of the hand accounting for aces. Used in both Dealer and Player
    blackjack: bool
        Whether the Dealer has a blackjack or not
    bust: bool
        Whether the Dealer is bust or not

    Methods
    -------
    clear_cards
        Clear all the cards for the hand
    deal
        If card hit twice
    hit
        Take 1 card from the deck
    hit_by_key
        Take 1 card from the deck based on the given card key
    evaluate
        Play the Dealer's hand
    show_cards
        Print the Dealer's hand to the log
    """

    def __init__(self, game, player=None):
        """
        Parameters
            * game -- the current game in play
            * player -- the player associated with this hand, if applicable
        """
        self.game = game
        self.player = player
        self.cards = []

    def __str__(self):
        hand_string = " ".join(str(card) for card in self.cards)
        return f"[{hand_string}] {self.value}"

    def __repr__(self):
        return f"Dealer(game={self.game})"

    def __len__(self):
        return len(self.cards)

    def __setitem__(self, position):
        return self.cards[position]

    def __getitem__(self, position):
        return self.cards[position]

    @property
    def value(self) -> list:
        return self._make_values([card.value for card in self.cards])

    @property
    def blackjack(self) -> bool:
        return len(self) == 2 and max(self.value) == 21

    @property
    def bust(self) -> bool:
        return min(self.value) > 21

    @staticmethod
    def _make_values(card_list: list) -> list:
        """Get the list-value of the hand accounting for aces"""
        sum_list = sum(card_list)
        if 1 in card_list and sum_list < 12:
            return [sum_list, sum_list + 10]
        else:
            return [sum_list]

    # def clear_cards(self):
    #     self.cards = []

    def hit(self):
        """Add a single Card to self.cards"""
        self.cards += self.game.deck.take_card(1)

    def deal(self):
        """Hit twice -- consider removing"""
        if len(self) == 0:
            [self.hit() for _ in range(2)]
        else:
            raise ValueError("This hand has already been dealt to")

    def _hit_by_key(self, key):
        """For debugging and testing"""
        self.cards += self.game.deck.take_card_by_key(key)

    def _deal_by_keys(self, keys):
        """For debugging and testing"""
        [self._hit_by_key(key) for key in keys]

    def evaluate(self):
        """Empty method that must be overridden by subclasses"""
        raise NotImplementedError(
            "The evaluate method needs to be implemented for this subclass"
        )

    def show_cards(self):
        """Print the cards in the hand to the terminal in a human-readable way"""
        # hand_string = ' '.join(str(card) for card in self.cards)
        # print(f'{self.player.name}\'s hand:\n\t[{hand_string}] {self.value}')
        print(f"{self.player.name}'s hand:")
        print(f'\t[{" ".join(str(card) for card in self.cards)}] {self.value}')


class Dealer(Hand):
    """
    A class to represent the House dealer in Blackjack. Inherits Hand
    """

    def __init__(self, game):
        super().__init__(game)

    def __str__(self):
        if len(self) == 0:
            return "[]"
        else:
            return f"Dealer's hand:\n\t[{self.cards[0]} ??] [{self.cards[0].value}]\n"

    def evaluate(self):
        while True:
            if self.game.verbose:
                self.show_cards()
            if max(self.value) >= 17:
                break
            self.hit()

    def show_cards(self):
        hand_string = " ".join(str(card) for card in self.cards)
        print(f"Dealer's hand:\n\t[{hand_string}] {self.value}\n")


class PlayerHand(Hand):
    """
    A class to represent the player's hand(s) in Blackjack. Inherits Hand
    """

    def __init__(self, player, bet):
        super().__init__(player.game, player)
        self.bet = bet
        self.from_split = False
        self.outcome = ""
        self.playing = True

    @property
    def option_key(self) -> (str, str):
        """
        Options to give the player when playing hand

        Return the following option keys based on the current cards and bet:
            *     'bust': Player is bust -- no options
            *       'bj': Player has blackjack and dealer has no ace -- no options
            *      't-s': Take, Stand (Player has blackjack and dealer has an ace)
            * 'h-s-d-sp': Hit, Stand, Double-Down, Split
            *    'h-s-d': Hit, Stand, Double-Down
            *      'h-s': Hit, Stand
        """
        if self.bust:
            return "bust", "Bust! You lose"
        elif self.blackjack:
            if self.player.game.dealer.cards[0].value == 1:
                return "t-s", "Take 1:1 payout [t] or stand [s]?"
            else:
                return "bj", "Blackjack! You win"
        elif len(self) == 2 and self.player.money > self.bet:
            if self[0].value == self[1].value:
                return "h-s-d-sp", "Hit [h], stand [s], double down [d], or split [sp]?"
            else:
                return "h-s-d", "Hit [h], stand [s], or double down [d]?"
        else:
            return "h-s", "Hit [h] or stand [s]?"

    def play_hand(self):
        """Play the hand -- has 3 parts: player choices, evaluate, then feedback"""
        # split from aces should never come down here
        while self.playing:
            print(f"Playing hand {str(self)}")

            opt_key, opt_text = self.option_key
            if opt_key in ["bust", "bj"]:
                self.playing = False
                break

            decision_key = input(opt_text).upper()

            if decision_key == "T":
                self.playing = False
            elif decision_key == "H":
                self.hit()
            elif decision_key == "S":
                self.playing = False
            elif decision_key == "D":
                self.hit()
                self.playing = False
            elif decision_key == "SP":
                self.split()
            else:
                print(f"Key {opt_key} not recognised, try again.")

        self.evaluate()
        # self.provide_feedback()

    def evaluate(self):
        hand_value = max(self.value)
        dealer_value = max(self.player.game.dealer.value)

        if hand_value > 21:
            self.outcome = "lose"
        elif self.player.dealer.blackjack:
            if self.blackjack:
                self.outcome = "draw"
            else:
                # assuming that dealer blackjack beats player 21
                print("Dealer has blackjack")
                self.outcome = "lose"
        elif dealer_value > 21:
            self.outcome = "win"
        elif hand_value < dealer_value:
            self.outcome = "lose"
        elif hand_value == dealer_value:
            self.outcome = "draw"
        elif hand_value > dealer_value:
            self.outcome = "win"
        else:
            raise AssertionError("Unexpected value in 'outcome' property")

    def split(self):
        if len(self) != 2:
            raise AssertionError(f"Can't split a hand with {len(self)} cards")
        elif self[0].rank != self[1].rank:
            raise AssertionError(
                f"Can't split a hand with cards {self[0]} and {self[1]}"
            )

        new_hand = self.player.add_hand(bet=self.bet)
        new_hand.cards.append(self.cards.pop(1))
        self.hit()
        new_hand.hit()
        if self[0].value == 1:
            # splitting A only gets one card each
            self.playing = False
            new_hand.playing = False


class Player:
    """
    Docs here
    """

    def __init__(self, game, name=None, money=500):
        self.game = game
        self.name = name or f"Player_{str(1 + game.player_count)}"
        self.money = money
        self.hands = []
        # TODO: need to include insurance somewhere
        self.insurance = 0

    def __str__(self):
        use_s = ["", "s"]
        ret_str = f"{self.name} has £{self.money} with hand{use_s[len(self) != 1]}:"
        for hand in self.hands:
            ret_str += f"\n\t {hand}  stake: £{hand.bet}"
        return ret_str + "\n"

    def __len__(self):
        return len(self.hands)

    def __setitem__(self, position):
        return self.hands[position]

    def __getitem__(self, position):
        return self.hands[position]

    def add_hand(self, bet=-1) -> PlayerHand:
        stake = bet
        if bet < 0:
            stake = self.game.min_bet
        new_hand = PlayerHand(player=self, bet=stake)
        self.hands.append(new_hand)
        return new_hand

    def clear_hands(self):
        self.hands = []

    def add_money(self, amount):
        assert type(amount) == int
        self.money += amount
        if self.game.verbose:
            print(
                f"{self.name} " + ["won", "lost"][amount < 0] + " " + str(abs(amount))
            )

    def print_money(self):
        print(f"{self.name} has {str(self.money)} money")

    @classmethod
    def new(cls, *args, **kwargs):
        return cls(*args, **kwargs)
