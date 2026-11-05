# jayforces

A small, self hosted contest app for practicing the kind of Python you write at work:
event processing, stateful classes, parsers, and classic ML written from scratch.
It looks like LeetCode, but most problems are closer to a laptop interview than a puzzle.

```bash
git clone <this repo> jayforces && cd jayforces
docker compose up --build
```

Open http://localhost:8000 and hit **Generate contest**.

The first build takes a few minutes because it downloads CPU-only PyTorch (about 200 MB).
Contest history is a SQLite file in `./data`, so it survives restarts and rebuilds.
Delete `data/jayforces.db` to start fresh.

## How a contest works

- You get four questions: one easy, two medium, one hard, and 90 minutes.
  The picker prefers questions you've seen the fewest times and tries to mix coding and ML.
- Questions come in parts. You only see Part 1 at first. When every test you can see passes,
  the next part unlocks and its requirements show up in the description. That's on purpose:
  part 2 usually asks you to extend what you wrote, so how you structured part 1 matters.
- The score for a question is passed tests over **all** its tests, including locked parts,
  so 100% means everything is done. The contest score is the average of your best runs.
- The next question opens once the current one hits 100%.
- `Ctrl+Enter` (or `Cmd+Enter`) runs the tests. Code autosaves as you type, and
  reloading the page drops you back where you were.

## The question bank

70 questions so far, 30 coding, 30 ML and 10 notebook questions, each with at least 15 tests:

|          | easy | medium | hard |
|----------|-----:|-------:|-----:|
| coding   |   10 |     12 |    8 |
| ml       |   10 |     12 |    8 |
| notebook |    3 |      4 |    3 |

Coding covers things like event streams and state machines, rate limiters, caches,
time-versioned stores, decorators, parsing messy CSVs and logs, shortest paths and simulations.
ML covers metrics, preprocessing, KNN, linear and logistic regression, PCA, naive Bayes, trees,
k-means, DBSCAN, HMMs, optimizers, hand-written backprop, a mini autograd, and a few PyTorch
questions (training loops, datasets and padding, multi-head attention).

## Notebook questions

Ten data science tasks (housing prices, card fraud, cart conversion, loan default, telecom churn, delivery ETA,
hospital readmission, auto claim cost, flight delays, ad clicks) live in `questions/ds/`. When one comes up in a contest,
the Monaco editor is replaced by JupyterLab (embedded from port 8888) with a notebook and a freshly generated random dataset
(`train.csv` with the target, `test.csv` with hidden labels). The same contest timer keeps running; you run cells as usual.

- Each dataset has 14 to 15 features, 6 to 8 categorical and the rest numeric or boolean. It is deliberately messy: numbers
  stored as text (`$1,234.50`, `1,200 sqft`, `45.3%`), booleans as `Y`/`yes`/`1`, labels with random case and spacing, several
  spellings of missing (`NaN`, `?`, `--`, `unknown`) and fake values like `-1` or `9999`.
- You define `clean(df)` (Part 1, checked cell by cell against the ground truth) and `fit_predict(train, test)` (Parts 2 and 3,
  scored on the hidden labels, plus robustness checks). **Run tests** reads the saved notebook (autosave is 5 s, `Ctrl+S` saves
  now) and runs it top to bottom like *Restart and run all*, so keep slow exploration cells out of it.
- The image has pandas, numpy, scikit-learn, LightGBM, XGBoost, scipy, matplotlib and seaborn.
- Each attempt gets its own folder in `data/notebooks/c<contest>_q<n>/`, so you can open it later. Without JupyterLab
  installed the server skips notebook questions.

To add one, create `questions/ds/<slug>/` with `question.md` (`kind: notebook`, `category: ds`), `data.py` (a `make(rng, n)` that
returns the clean data plus `KINDS`, `SENTINEL`, `MISSING`, `SCORES`, see `app/dsgen.py`), `solution.py` (reference `clean` and
`fit_predict`) and a two line `tests.py` (`from dscheck import suite; suite(globals())`). Then run `check_bank.py` on it.

## Adding a question

Make a folder anywhere under `questions/` (I keep `coding/` and `ml/` apart, the app doesn't care):

```
questions/coding/surge_alerts/
  question.md
  solution.py
  tests.py
```

**question.md** has a small header and then the statement. Everything before the first
`## Part` heading is always shown. Each `## Part N: ...` section unlocks in order.

```markdown
---
title: Surge alerts
difficulty: medium        # easy | medium | hard
category: coding          # coding | ml
tags: events, windows
timeout: 3                # optional, seconds per test (default 3)
---
Some context that's always visible.

## Part 1: The basics
...

## Part 2: The twist
...
```

**solution.py** is your reference answer. The starter code people see is generated from it:
imports, UPPER_CASE constants, function and class signatures and docstrings are kept, bodies
become `raise NotImplementedError`, and anything starting with `_` is dropped. So put the
hints you want people to see in docstrings, and name private helpers with a leading underscore.
If you'd rather hand-write the starter, add a `starter.py` and it wins.

**tests.py** has plain functions named `test_p<part>_<name>(sol)`, where `sol` is the user's
module. The part number decides when a test unlocks. Helpers live in `app/check.py`:

```python
from check import eq, close, raises, table

def test_p1_basic(sol):
    eq(sol.alerts([("z1", 5)]), ["z1"])

def test_p2_rejects_negative(sol):
    raises(ValueError, sol.alerts, [("z1", -1)])

# lots of small cases: (name, args, expected). An exception class as expected means "must raise".
table(globals(), 1, lambda s, events: s.alerts(events), [
    ("empty", [], []),
    ("quiet zone", [("z1", 0)], []),
])
```

`eq` compares floats and numpy arrays with a tolerance and prints a readable expected/got diff.

Since `./questions` is mounted into the container, new questions show up on the next contest,
no rebuild needed. Before you rely on one, check it:

```bash
docker compose run --rm jayforces python app/check_bank.py surge_alerts
```

That confirms the reference solution scores 100%, the generated starter loads but fails,
every part has tests, and there are at least 15 of them. Run it with no arguments to check the
whole bank.

## Layout

```
app/
  server.py       http server and contest logic (standard library only)
  questions.py    loads question folders, builds starter code
  runner.py       runs one question's tests in a subprocess, one timeout per test
  check.py        assertion helpers for tests
  check_bank.py   validates questions
  notebooks.py    notebook questions: notebook file, JupyterLab, grading a saved notebook
  dsgen.py        random messy datasets for notebook questions
  dscheck.py      shared tests for notebook questions
  static/         the page: index.html, app.js, style.css, vendored marked.js
questions/        the bank
data/             sqlite lives here (git ignored)
```

## Notes

- The code editor (Monaco) and the fonts load from a CDN, so the browser needs internet.
  Without it you get a plain text editor and system fonts, and everything else still works.
- Your code runs as a subprocess inside the container with no extra sandboxing. That's fine for
  practicing on your own machine; don't expose this to the internet.
- `CONTEST_MINUTES` in `docker-compose.yml` changes the contest length.
- Running without Docker works too if you have numpy and torch (plus pandas, scikit-learn, lightgbm and jupyterlab for
  the notebook questions): `python app/server.py`.
- JupyterLab runs without a token on port 8888 (`JUPYTER_PORT` changes it). Like the code runner, don't expose it.
