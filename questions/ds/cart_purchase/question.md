---
title: Will this session buy?
difficulty: easy
category: ds
kind: notebook
tags: ecommerce, conversion, cleaning
timeout: 90
---
An online store wants to know which browsing sessions will end in a purchase, so it can show a nudge or a discount only where it helps. Each row is one session, logged by the web and the mobile app (which format values differently). Predict `purchased` for the sessions in `test.csv`.

Work in the notebook on the right. It has `train.csv` (with the target) and `test.csv` (features only, the labels are hidden), and
the environment has pandas, numpy, scikit-learn and LightGBM ready. The data was generated at random for this attempt and is
**deliberately messy**: numbers stored as text, booleans written many ways, inconsistent labels, several spellings of missing, and some
fake values. Trust `info()`, `value_counts()` and your eyes, not the data dictionary alone.

| feature | type | meaning |
|---|---|---|
| `traffic_source` | category | Where the visit came from |
| `device` | category | Device class |
| `country` | category | Visitor country |
| `browser` | category | Browser family |
| `landing_category` | category | Category of the first page |
| `customer_segment` | category | Customer history segment |
| `pages_viewed` | number | Pages viewed in the session |
| `session_minutes` | number | Session length in minutes |
| `cart_value` | number (dollars) | Value of the cart in dollars |
| `items_in_cart` | number | Items in the cart |
| `prior_orders` | number | Orders placed before this session |
| `is_logged_in` | yes / no | Visitor was logged in |
| `has_coupon` | yes / no | A coupon was applied |
| `is_weekend` | yes / no | Session happened on a weekend |

Target: `purchased` (1 = bought something in this session). `prior_orders` is `-1` when the CRM lookup failed.

## Part 1: Clean the data

Write `clean(df)`. It receives a raw frame exactly as `pd.read_csv` returns it (with or without the target column) and returns a cleaned **copy**:

- numeric columns stored as text become floats: strip currency symbols, thousands separators, units and percent signs
- boolean columns become `1.0` / `0.0`, whatever the spelling was
- categorical columns become lowercase, trimmed, with spaces and hyphens turned into underscores (`"Heat Pump"` and `" heat-pump "` become `heat_pump`), in the pandas `category` dtype
- every kind of missing value, and every fake "unknown" value listed above, becomes `NaN`. Do not impute and do not drop rows
- all columns stay, the index stays, the target is untouched, the input is not modified, and running it twice is safe

Every feature has its own test, so you can see which column is still wrong.

## Part 2: A first model

Write `fit_predict(train, test)`. `train` is the raw training frame including `purchased`, `test` is the raw test frame. Clean both, train anything you like
(LightGBM, scikit-learn, ...) and return a 1-D array with the predicted probability of class 1 for every test row.
Score: ROC AUC on the hidden labels. It must reach **0.7**, then **0.74**. Predictions must be finite and between 0 and 1, and the frames you were given must not be modified.

## Part 3: Make it solid

Reach ROC AUC **0.76**. Then make it robust: the function must still work when `test` contains a label never seen in training and rows where
every feature is missing, and two runs must give the same predictions (set your seeds).
