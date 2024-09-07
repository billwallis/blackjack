"""
Constants for the blackjack game.
"""

BLACKJACK = 21
BLACKJACK_CARD_COUNT = 2
DOUBLE_DOWN_CARD_COUNT = 2
DEALER_LOWER_LIMIT = 17


# https://stackoverflow.com/a/39452138/8213085
class Colours:
    """
    ANSI escape codes for colours in the terminal.
    """

    END = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    BLUE = "\033[34m"
    FAIL = "\033[91m"
    PASS = "\033[92m"  # noqa: S105
    WARN = "\033[93m"
