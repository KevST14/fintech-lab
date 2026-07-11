"""A Money type that doesn't lose pennies.

Read README.md first. test_money.py says what this has to do; the method
bodies are yours to write, and you can restructure the class however you like
(a frozen dataclass is a good start) as long as the tests pass.

Public attributes: `amount` (a Decimal) and `currency` (an ISO 4217 code).
"""

from decimal import ROUND_HALF_EVEN, Decimal

# ISO 4217 minor units: digits after the decimal point for each currency.
MINOR_UNITS = {"GBP": 2, "USD": 2, "EUR": 2, "JPY": 0, "KWD": 3}


class CurrencyMismatch(ValueError):
    """Raised when combining amounts in different currencies."""


class Money:
    def __init__(self, amount: str | int | Decimal, currency: str = "GBP") -> None:
        raise NotImplementedError

    def __add__(self, other: "Money") -> "Money":
        raise NotImplementedError

    def __sub__(self, other: "Money") -> "Money":
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def multiply(self, factor: str | int | Decimal, rounding: str = ROUND_HALF_EVEN) -> "Money":
        """Multiply by a rate and round back to the currency's minor unit."""
        raise NotImplementedError

    def split(self, n: int) -> list["Money"]:
        """Split into n shares that add up exactly. Leftover minor units go to the first shares."""
        raise NotImplementedError

    def allocate(self, ratios: list[int]) -> list["Money"]:
        """Split by ratio. Shares add up exactly, and a share with ratio 0 gets nothing."""
        raise NotImplementedError
