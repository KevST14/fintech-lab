# 001: Money precision

> Why do banks never store money as a float?

**Track:** Banking · **Status:** Not started

## Why this matters

Every payment system stores amounts, adds them up, applies interest and FX rates, and splits bills, fees and refunds. Lose one penny per transaction and at bank volumes that's millions of pennies a day, and the ledger stops balancing. Balancing exactly is the one thing a ledger has to do.

## Tasks

Work through the parts in order. Run one part's tests with `-k`, e.g.

```bash
uv run pytest experiments/001-money-precision -k Construction
```

### Part 1: Make floats break (notebook)

In `explore.ipynb`, find at least three *different* ways `float` gets money wrong. Predict each answer before you run it. Then explain in your own words why it happens. What is it about how a float is stored?

### Part 2: A `Money` type (`money.py`, `TestConstruction` + `TestArithmetic`)

Build an immutable `Money` with an amount and an [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) currency. First decide how to store the amount: a `Decimal`, or a whole number of minor units (pence, cents) as an `int`. Both are used in real systems. Write down which one you chose and why before you start.

What the tests check:

- It can be built from a string, an int or a `Decimal`. A float raises `TypeError`, because once a value is a float the damage is already done.
- An amount with more decimal places than the currency allows (`"2.675"` in GBP) raises `ValueError`. JPY has 0 decimal places and KWD has 3.
- `.amount` gives back a `Decimal` and `.currency` gives back the code.
- Adding two different currencies raises `CurrencyMismatch`.
- `str()` looks like `"5.00 GBP"`.
- Equal amounts are equal and hash the same.

### Part 3: Multiplying and rounding (`TestMultiply`)

Interest, fees and FX all multiply money by a rate, and the answer usually doesn't fit in whole pennies. `multiply(factor, rounding)` rounds back to the currency's minor unit, using a rounding mode from the `decimal` module. The default is `ROUND_HALF_EVEN`. Find out what that does and why it's called banker's rounding. Part 5 tests whether it matters.

### Part 4: Splitting without losing a penny (`TestSplit` + `TestAllocate`)

Split £100 three ways and you get 33.33 + 33.33 + 33.33 = 99.99. Where did the penny go?

- `split(n)` divides the amount into `n` shares that add back up to the original exactly. Leftover pennies go to the first shares, so £100 becomes 33.34, 33.33, 33.33.
- `allocate(ratios)` splits by ratio, like a 70/30 fee share. The shares must add up exactly, each must be within one minor unit of its exact share, and a share with ratio 0 gets nothing. If two shares tie for a leftover penny, the earlier one gets it.

### Part 5: Does the rounding rule matter? (notebook)

Simulate a million interest payments. Round them once with `ROUND_HALF_UP` and once with `ROUND_HALF_EVEN`, and compare the total rounding error. Predict the result first, then chart it.

### Stretch

- Write a [Hypothesis](https://hypothesis.readthedocs.io/) property test: for *any* amount and any `n`, `split(n)` adds back up to the original. Let it hunt for a counterexample.
- What should `Money("-10.00").split(3)` return? Refunds are negative. Check what your code does and decide whether it's right.
- Implement the other storage choice (int vs `Decimal`) and time both in the notebook.

<details>
<summary>Stuck? Hints (try first)</summary>

- **Part 1:** add a small amount many times. Use Python's built-in `round()` on an amount ending in 5. Try a very large amount in pence.
- **Part 2:** a frozen `dataclass` gives you immutability and `__hash__` for free. A `__repr__` makes pytest's failure messages much easier to read. To check decimal places, look at `Decimal.as_tuple().exponent`, and watch out for `"2.670"`.
- **Part 3:** `Decimal.quantize(..., rounding=...)`. Work out the quantum from the currency's minor units instead of hard-coding `0.01`.
- **Part 4:** do the splitting in whole minor units (ints). Integer division leaves a whole number of leftover pennies, so all you have to decide is who gets them. If a zero-ratio share ends up with a penny, look at *how* you hand out the leftovers, then look up the largest remainder method.

</details>

## What I expected

_Write this before starting._

## Attempt log

_Dated, short._

## What broke

## Result

_The Part 5 numbers and chart, and which storage you chose and why._

## What I'd do next

## Reading

- [Floating Point Arithmetic: Issues and Limitations](https://docs.python.org/3/tutorial/floatingpoint.html), Python docs
- [`decimal` module](https://docs.python.org/3/library/decimal.html), especially the rounding modes
- [The Floating-Point Guide](https://floating-point-gui.de/)
- [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217): currency codes and minor units
- [Money pattern](https://martinfowler.com/eaaCatalog/money.html), Martin Fowler, where the allocate idea comes from
