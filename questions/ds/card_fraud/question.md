---
title: Card fraud scoring
difficulty: hard
category: ds
kind: notebook
tags: payments, fraud, imbalanced
timeout: 90
---
A payments processor scores every card transaction in real time. Only about 5% are fraud, and the feed comes from several acquirers that format things their own way. Rank the transactions in `test.csv` so the riskiest come first.

Work in the notebook on the right. It has `train.csv` (with the target) and `test.csv` (features only, the labels are hidden), and
the environment has pandas, numpy, scikit-learn and LightGBM ready. The data was generated at random for this attempt and is
**deliberately messy**: numbers stored as text, booleans written many ways, inconsistent labels, several spellings of missing, and some
fake values. Trust `info()`, `value_counts()` and your eyes, not the data dictionary alone.

| feature | type | meaning |
|---|---|---|
| `merchant_category` | category | Merchant type |
| `card_type` | category | Debit, credit, prepaid or virtual |
| `channel` | category | How the card was used |
| `merchant_country` | category | Merchant location relative to the cardholder |
| `device_os` | category | Operating system of the device used |
| `card_network` | category | Card network |
| `issuer_tier` | category | Card product tier |
| `amount` | number (dollars) | Transaction amount in dollars |
| `acct_age_days` | number | Age of the account in days |
| `txn_count_24h` | number | Transactions on this card in the last 24 hours |
| `avg_amount_30d` | number (dollars) | Average transaction amount over the last 30 days, in dollars |
| `dist_from_home_km` | number | Distance from the cardholder home in km |
| `is_card_present` | yes / no | Physical card was present |
| `is_new_merchant` | yes / no | First time this card is used at the merchant |
| `billing_zip_match` | yes / no | Billing ZIP matches the one on file |

Target: `is_fraud` (1 = confirmed fraud). `acct_age_days` is `-1` when the account record was missing.

## Part 1: Clean the data

Write `clean(df)`. It receives a raw frame exactly as `pd.read_csv` returns it (with or without the target column) and returns a cleaned **copy**:

- numeric columns stored as text become floats: strip currency symbols, thousands separators, units and percent signs
- boolean columns become `1.0` / `0.0`, whatever the spelling was
- categorical columns become lowercase, trimmed, with spaces and hyphens turned into underscores (`"Heat Pump"` and `" heat-pump "` become `heat_pump`), in the pandas `category` dtype
- every kind of missing value, and every fake "unknown" value listed above, becomes `NaN`. Do not impute and do not drop rows
- all columns stay, the index stays, the target is untouched, the input is not modified, and running it twice is safe

Every feature has its own test, so you can see which column is still wrong.

## Part 2: A first model

Write `fit_predict(train, test)`. `train` is the raw training frame including `is_fraud`, `test` is the raw test frame. Clean both, train anything you like
(LightGBM, scikit-learn, ...) and return a 1-D array with the predicted probability of class 1 for every test row.
Score: average precision (area under the precision recall curve) on the hidden labels. It must reach **0.2**, then **0.27**. Predictions must be finite and between 0 and 1, and the frames you were given must not be modified.

## Part 3: Make it solid

Reach average precision (area under the precision recall curve) **0.3**. Then make it robust: the function must still work when `test` contains a label never seen in training and rows where
every feature is missing, and two runs must give the same predictions (set your seeds).
