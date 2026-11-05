---
title: Telecom churn
difficulty: easy
category: ds
kind: notebook
tags: telecom, churn, cleaning
timeout: 90
---
A mobile and broadband provider wants to find customers likely to cancel in the next month so retention can call them first. The billing export mixes formats from two systems. Predict `churned` for the customers in `test.csv`.

Work in the notebook on the right. It has `train.csv` (with the target) and `test.csv` (features only, the labels are hidden), and
the environment has pandas, numpy, scikit-learn and LightGBM ready. The data was generated at random for this attempt and is
**deliberately messy**: numbers stored as text, booleans written many ways, inconsistent labels, several spellings of missing, and some
fake values. Trust `info()`, `value_counts()` and your eyes, not the data dictionary alone.

| feature | type | meaning |
|---|---|---|
| `contract` | category | Contract type |
| `internet_service` | category | Internet product |
| `payment_method` | category | How the customer pays |
| `plan` | category | Mobile plan tier |
| `region` | category | Sales region |
| `acquisition_channel` | category | How the customer signed up |
| `tenure_months` | number | Months as a customer |
| `monthly_charges` | number (dollars) | Monthly bill in dollars |
| `total_charges` | number (dollars) | Total billed so far in dollars |
| `support_calls_90d` | number | Calls to support in the last 90 days |
| `data_gb` | number | Data used last month in GB |
| `paperless_billing` | yes / no | Uses paperless billing |
| `has_tech_support` | yes / no | Has the tech support add-on |
| `has_multiple_lines` | yes / no | Has more than one line |
| `is_senior` | yes / no | Senior citizen discount |

Target: `churned` (1 = cancelled). `support_calls_90d` is `-1` when the call log was unavailable.

## Part 1: Clean the data

Write `clean(df)`. It receives a raw frame exactly as `pd.read_csv` returns it (with or without the target column) and returns a cleaned **copy**:

- numeric columns stored as text become floats: strip currency symbols, thousands separators, units and percent signs
- boolean columns become `1.0` / `0.0`, whatever the spelling was
- categorical columns become lowercase, trimmed, with spaces and hyphens turned into underscores (`"Heat Pump"` and `" heat-pump "` become `heat_pump`), in the pandas `category` dtype
- every kind of missing value, and every fake "unknown" value listed above, becomes `NaN`. Do not impute and do not drop rows
- all columns stay, the index stays, the target is untouched, the input is not modified, and running it twice is safe

Every feature has its own test, so you can see which column is still wrong.

## Part 2: A first model

Write `fit_predict(train, test)`. `train` is the raw training frame including `churned`, `test` is the raw test frame. Clean both, train anything you like
(LightGBM, scikit-learn, ...) and return a 1-D array with the predicted probability of class 1 for every test row.
Score: ROC AUC on the hidden labels. It must reach **0.78**, then **0.82**. Predictions must be finite and between 0 and 1, and the frames you were given must not be modified.

## Part 3: Make it solid

Reach ROC AUC **0.845**. Then make it robust: the function must still work when `test` contains a label never seen in training and rows where
every feature is missing, and two runs must give the same predictions (set your seeds).
