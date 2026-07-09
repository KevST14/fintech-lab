# fintech-lab

Small experiments in the engineering behind banks and trading firms. Each one starts from a question I couldn't answer yet, and keeps the attempts that didn't work next to the one that did.

## How each experiment works

1. **Question.** One thing I don't understand, e.g. "why do banks never store money as a float?"
2. **Predict.** Write down what I expect *before* running anything.
3. **Break it.** Try the naive version in the notebook (`explore.ipynb`) and find where it goes wrong.
4. **Fix it.** Build the proper version as a module with tests. The failing test gets committed before the fix.
5. **Measure.** Real numbers or a chart, not "it works now".
6. **Write it up.** What broke, what I learned, what I'd do next, in the experiment's README.

Notebooks are for exploring and showing results. The `.py` files and tests are the real implementation.

## Roadmap

| # | Experiment | Question | Track | Status |
|---|---|---|---|---|
| 001 | [Money precision](experiments/001-money-precision/) | Why do banks never store money as a float? | Banking | Next up |
| 002 | Limit order book | How does an exchange decide who trades with whom? | Markets | Planned |
| 003 | The 99.8% accurate fraud model | Why can a fraud model be 99.8% accurate and useless? | AI & data | Planned |
| 004 | Lost updates | What happens when two payments hit the same account at once? | Banking | Planned |
| 005 | Too good to be true | Why does my backtest make 400% a year? | Markets | Planned |
| 006 | Market data with DuckDB | How do you turn raw trades into price bars and VWAP? | AI & data | Planned |
| 007 | Pay exactly once | How does a payment API survive retries without charging twice? | Banking | Planned |
| 008 | Pricing an option three ways | Do Black-Scholes, a binomial tree and Monte Carlo agree? | Markets | Planned |
| 009 | Ask a 10-K | Can an LLM answer questions about an annual report, and how do I tell when it's wrong? | AI & data | Planned |
| 010 | Reading FIX and ISO 20022 | What do the messages banks and exchanges send each other look like? | Banking | Planned |
| 011 | Value at Risk | How much could a portfolio lose on a bad day, and was the estimate right? | Markets | Planned |
| 012 | Testing an LLM agent | How do you measure whether an agent with tools gets the right answer? | AI & data | Planned |

The roadmap will change as I go. Questions that come up during one experiment often become the next one.

## Running it

Needs [uv](https://docs.astral.sh/uv/).

```bash
uv sync                                    # install everything
uv run pytest experiments/001-money-precision   # one experiment's tests
uv run jupyter lab                         # open the notebooks
```

## Learning log

Dated notes on what I worked on and what surprised me: [LOG.md](LOG.md).
