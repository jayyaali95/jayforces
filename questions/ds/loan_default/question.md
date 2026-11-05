---
title: Loan default risk
difficulty: medium
category: ds
kind: notebook
tags: lending, risk, cleaning
timeout: 90
---
A consumer lender wants to estimate the chance that a funded loan defaults, to price loans and cap exposure. Applications arrive from a partner export where money and rates are text. Predict `defaulted` for the loans in `test.csv`.

Work in the notebook on the right. It has `train.csv` (with the target) and `test.csv` (features only, the labels are hidden), and
the environment has pandas, numpy, scikit-learn and LightGBM ready. The data was generated at random for this attempt and is
**deliberately messy**: numbers stored as text, booleans written many ways, inconsistent labels, several spellings of missing, and some
fake values. Trust `info()`, `value_counts()` and your eyes, not the data dictionary alone.

| feature | type | meaning |
|---|---|---|
| `purpose` | category | Stated purpose of the loan |
| `home_ownership` | category | Rent, own or mortgage |
| `emp_length` | category | Employment length bucket (`lt_1y`, `y1_3`, `y4_6`, `y7_9`, `y10_plus`) |
| `verification` | category | Income verification status |
| `term` | category | Loan term, `m36` or `m60` months |
| `region` | category | US region |
| `application_type` | category | Individual or joint application |
| `loan_amount` | number (dollars) | Loan amount in dollars |
| `annual_income` | number (dollars) | Stated annual income in dollars |
| `dti` | number | Debt to income ratio in percent points |
| `interest_rate` | number (percent) | Interest rate in percent |
| `revolving_util` | number (percent) | Revolving credit utilization in percent |
| `open_accounts` | number | Open credit accounts |
| `credit_history_years` | number | Length of credit history in years |
| `has_delinq_2y` | yes / no | Any delinquency in the last two years |

Target: `defaulted` (1 = charged off). `credit_history_years` is `-1` when the bureau had no file.

## Part 1: Clean the data

Write `clean(df)`. It receives a raw frame exactly as `pd.read_csv` returns it (with or without the target column) and returns a cleaned **copy**:

- numeric columns stored as text become floats: strip currency symbols, thousands separators, units and percent signs
- boolean columns become `1.0` / `0.0`, whatever the spelling was
- categorical columns become lowercase, trimmed, with spaces and hyphens turned into underscores (`"Heat Pump"` and `" heat-pump "` become `heat_pump`), in the pandas `category` dtype
- every kind of missing value, and every fake "unknown" value listed above, becomes `NaN`. Do not impute and do not drop rows
- all columns stay, the index stays, the target is untouched, the input is not modified, and running it twice is safe

Every feature has its own test, so you can see which column is still wrong.

## Part 2: A first model

Write `fit_predict(train, test)`. `train` is the raw training frame including `defaulted`, `test` is the raw test frame. Clean both, train anything you like
(LightGBM, scikit-learn, ...) and return a 1-D array with the predicted probability of class 1 for every test row.
Score: ROC AUC on the hidden labels. It must reach **0.62**, then **0.67**. Predictions must be finite and between 0 and 1, and the frames you were given must not be modified.

## Part 3: Make it solid

Reach ROC AUC **0.69**. Then make it robust: the function must still work when `test` contains a label never seen in training and rows where
every feature is missing, and two runs must give the same predictions (set your seeds).
