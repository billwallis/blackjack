"""
Blackjack-specific rules and logic.
"""

from __future__ import annotations

from blackjack import constants, participants
from blackjack import deck as deck_


def play_hand__dealer(
    dealer_hand: participants.Hand,
    deck: deck_.Deck,
) -> None:
    """
    Play the dealer's hand.

    The dealer must hit on 16 or less and stand on 17 or more.
    """
    while max(dealer_hand.values) < constants.DEALER_LOWER_LIMIT:
        dealer_hand.hit(deck)

    dealer_hand.playing = False


def play_hand__player(
    player_hand: participants.PlayerHand,
    dealer_hand: participants.Hand,
    player: participants.Player,
    deck: deck_.Deck,
) -> None:
    """
    Play the player's hand.
    """

    while player_hand.playing:
        print(f"\nPlaying hand {player_hand.show()!s}")

        options = get_options_for_player_hand(
            player,
            player_hand,
            dealer_hand[0].rank == 1,
        )
        if not options:
            player_hand.playing = False
            break

        player_options = ", ".join(option.readable for option in options) + "?"
        allowed_options = [option.value for option in options]

        decision_key = ""
        while decision_key not in allowed_options:
            decision_key = input(f"{player_options} ")

        decision = participants.PlayerOption(decision_key)
        print(f"Player chose {decision.name}")
        action(player_hand, decision, player, deck)


def action(
    player_hand: participants.PlayerHand,
    option: participants.PlayerOption,
    player: participants.Player,
    deck: deck_.Deck,
) -> None:
    """
    Resolve the actions on the player given the option.

    :param player_hand: The hand the player is playing.
    :param option: The option the player has chosen.
    :param player: The player making the choice.
    :param deck: The deck to draw from.
    """
    match option:
        case participants.PlayerOption.TAKE_INSURANCE:
            # TODO: Update their bet and money
            player_hand.playing = False
        case participants.PlayerOption.HIT:
            player_hand.hit(deck)
        case participants.PlayerOption.STAND:
            player_hand.playing = False
        case participants.PlayerOption.DOUBLE_DOWN:
            player_hand.hit(deck)
            player_hand.playing = False
        case participants.PlayerOption.SPLIT:
            player_hand.split(deck, player)


def get_options_for_player_hand(
    player: participants.Player,
    hand: participants.Hand,
    dealer_has_ace: bool,
) -> list[participants.PlayerOption]:
    """
    Options to give the player when playing their hand.

    :return: The list of the options to give.
    """
    if hand.bust or (hand.blackjack and not dealer_has_ace):
        return []

    options = [
        participants.PlayerOption.HIT,
        participants.PlayerOption.STAND,
    ]

    if _can_double_down(player, hand):
        options.append(participants.PlayerOption.DOUBLE_DOWN)

    if _can_split(player, hand):
        options.append(participants.PlayerOption.SPLIT)

    if _can_take_insurance(player, hand, dealer_has_ace):
        options.append(participants.PlayerOption.TAKE_INSURANCE)

    return options


def _can_double_down(
    player: participants.Player,
    hand: participants.Hand,
) -> bool:
    return (
        player.money >= (2 * hand.bet)
        and len(hand) == constants.DOUBLE_DOWN_CARD_COUNT
    )


def _can_split(
    player: participants.Player,
    hand: participants.Hand,
) -> bool:
    return hand[0].rank == hand[1].rank and player.money >= (2 * hand.bet)


def _can_take_insurance(
    player: participants.Player,
    hand: participants.Hand,
    dealer_has_ace: bool,
) -> bool:
    return (
        len(hand) == constants.DOUBLE_DOWN_CARD_COUNT
        and player.money >= (1.5 * hand.bet)
        and dealer_has_ace
    )


def get_hand_outcome(  # noqa: PLR0911
    hand: participants.Hand,
    dealer_hand: participants.Hand,
) -> participants.HandOutcome:
    """
    Evaluate the hand and update the outcome.
    """
    hand_value = max(hand.values.eligible_values, default=99)
    dealer_value = max(dealer_hand.values.eligible_values, default=99)

    if hand.bust:
        return participants.HandOutcome.LOSE

    if dealer_hand.bust:
        return participants.HandOutcome.WIN

    if dealer_hand.blackjack:
        # Assuming that dealer blackjack beats player 21
        if hand.blackjack:
            return participants.HandOutcome.DRAW
        return participants.HandOutcome.LOSE

    if hand_value > dealer_value:
        return participants.HandOutcome.WIN

    if hand_value == dealer_value:
        return participants.HandOutcome.DRAW

    return participants.HandOutcome.LOSE


def apply_outcome(
    player: participants.Player,
    outcome: participants.HandOutcome,
    bet: int,
) -> None:
    """
    Apply the outcome to the player's money.

    :param player: The player to apply the outcome to.
    :param outcome: The outcome of the hand.
    :param bet: The bet placed on the hand.
    """
    if outcome == participants.HandOutcome.WIN:
        player.money += bet
    elif outcome == participants.HandOutcome.LOSE:
        player.money -= bet
