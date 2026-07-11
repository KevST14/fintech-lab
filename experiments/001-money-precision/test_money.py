from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from functools import reduce
from operator import add

import pytest

from money import CurrencyMismatch, Money


def total(shares):
    return reduce(add, shares)


class TestConstruction:
    def test_from_string(self):
        m = Money("5", "GBP")
        assert m.amount == Decimal("5.00")
        assert m.currency == "GBP"

    def test_currency_defaults_to_gbp(self):
        assert Money("5") == Money("5.00", "GBP")

    def test_from_int_and_decimal(self):
        assert Money(5) == Money(Decimal("5.00")) == Money("5")

    def test_str_uses_the_currencys_minor_units(self):
        assert str(Money("5")) == "5.00 GBP"
        assert str(Money("1500", "JPY")) == "1500 JPY"
        assert str(Money("1.5", "KWD")) == "1.500 KWD"
        assert str(Money("-3.5")) == "-3.50 GBP"

    def test_float_is_rejected(self):
        with pytest.raises(TypeError):
            Money(0.1)

    def test_too_many_decimal_places_is_rejected(self):
        with pytest.raises(ValueError):
            Money("2.675", "GBP")
        with pytest.raises(ValueError):
            Money("100.5", "JPY")

    def test_trailing_zeros_are_fine(self):
        assert Money("2.670") == Money("2.67")

    def test_unknown_currency_is_rejected(self):
        with pytest.raises(ValueError):
            Money("1.00", "XYZ")

    def test_equal_amounts_hash_the_same(self):
        assert len({Money("1"), Money("1.00"), Money("1.0")}) == 1

    def test_same_amount_in_different_currencies_is_not_equal(self):
        assert Money("1.00", "GBP") != Money("1.00", "USD")


class TestArithmetic:
    def test_tenths_add_up_exactly(self):
        assert Money("0.10") + Money("0.20") == Money("0.30")

    def test_ten_lots_of_10p_make_a_pound(self):
        assert total([Money("0.10")] * 10) == Money("1.00")

    def test_subtract_can_go_negative(self):
        assert Money("5.00") - Money("7.50") == Money("-2.50")

    def test_adding_different_currencies_raises(self):
        with pytest.raises(CurrencyMismatch):
            Money("10.00", "GBP") + Money("5.00", "USD")

    def test_currency_mismatch_is_a_value_error(self):
        assert issubclass(CurrencyMismatch, ValueError)

    def test_adding_a_plain_number_raises(self):
        with pytest.raises(TypeError):
            Money("1.00") + 1


class TestMultiply:
    def test_exact_result_needs_no_rounding(self):
        assert Money("1000", "JPY").multiply("1.075") == Money("1075", "JPY")

    def test_half_up_rounds_a_tie_up(self):
        # 2.50 * 1.05 = 2.625
        assert Money("2.50").multiply("1.05", ROUND_HALF_UP) == Money("2.63")

    def test_half_even_rounds_a_tie_to_the_even_digit(self):
        assert Money("2.50").multiply("1.05", ROUND_HALF_EVEN) == Money("2.62")

    def test_default_rounding_is_half_even(self):
        # 997 * 0.5 = 498.5
        assert Money("997", "JPY").multiply("0.5") == Money("498", "JPY")

    def test_non_tie_rounds_to_nearest(self):
        assert Money("10.00").multiply("0.3337") == Money("3.34")

    def test_float_factor_is_rejected(self):
        with pytest.raises(TypeError):
            Money("1.00").multiply(1.05)


class TestSplit:
    def test_leftover_pennies_go_to_the_first_shares(self):
        assert Money("100.00").split(3) == [Money("33.34"), Money("33.33"), Money("33.33")]

    def test_shares_add_back_up(self):
        for amount in ["0.01", "0.05", "10.00", "99.99", "1234.56"]:
            for n in range(1, 8):
                shares = Money(amount).split(n)
                assert len(shares) == n
                assert total(shares) == Money(amount), (amount, n)

    def test_fewer_pennies_than_people(self):
        assert Money("0.02").split(3) == [Money("0.01"), Money("0.01"), Money("0.00")]

    def test_respects_minor_units(self):
        assert Money("100", "JPY").split(3) == [
            Money("34", "JPY"),
            Money("33", "JPY"),
            Money("33", "JPY"),
        ]

    def test_zero_or_negative_n_is_rejected(self):
        with pytest.raises(ValueError):
            Money("1.00").split(0)
        with pytest.raises(ValueError):
            Money("1.00").split(-2)


class TestAllocate:
    def test_seventy_thirty(self):
        assert Money("0.05").allocate([70, 30]) == [Money("0.04"), Money("0.01")]

    def test_equal_ratios_match_split(self):
        assert Money("100.00").allocate([1, 1, 1]) == Money("100.00").split(3)

    @pytest.mark.parametrize(
        "amount, ratios",
        [
            ("100.00", [70, 30]),
            ("0.05", [1, 1, 1]),
            ("10.00", [3, 2, 2]),
            ("999.99", [1, 2, 3, 4]),
            ("0.03", [50, 25, 25]),
        ],
    )
    def test_shares_add_up_and_stay_within_a_penny_of_exact(self, amount, ratios):
        m = Money(amount)
        shares = m.allocate(ratios)
        assert total(shares) == m
        for share, ratio in zip(shares, ratios):
            exact = m.amount * ratio / sum(ratios)
            assert abs(share.amount - exact) < Decimal("0.01"), (share, exact)

    def test_zero_ratio_gets_nothing(self):
        shares = Money("0.01").allocate([0, 1, 1])
        assert shares[0] == Money("0.00")
        assert total(shares) == Money("0.01")

    def test_bad_ratios_are_rejected(self):
        for ratios in ([], [0, 0], [1, -1]):
            with pytest.raises(ValueError):
                Money("1.00").allocate(ratios)
