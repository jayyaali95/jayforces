---
title: House price estimator
difficulty: easy
category: ds
kind: notebook
tags: housing, regression, cleaning
timeout: 90
---
A real estate site wants an instant estimate for every new listing. You get last year's sales scraped from several feeds, so the formats are inconsistent. Predict the sale price of the listings in `test.csv`.

Work in the notebook on the right. It has `train.csv` (with the target) and `test.csv` (features only, the labels are hidden), and
the environment has pandas, numpy, scikit-learn and LightGBM ready. The data was generated at random for this attempt and is
**deliberately messy**: numbers stored as text, booleans written many ways, inconsistent labels, several spellings of missing, and some
fake values. Trust `info()`, `value_counts()` and your eyes, not the data dictionary alone.

| feature | type | meaning |
|---|---|---|
| `neighborhood` | category | Area of town |
| `property_type` | category | House, condo, townhouse or duplex |
| `heating` | category | Main heating system |
| `condition` | category | Condition at listing time |
| `parking` | category | Parking available |
| `listing_source` | category | Who listed it |
| `sqft` | number | Living area in square feet |
| `bedrooms` | number | Bedroom count |
| `bathrooms` | number | Bathrooms, halves allowed |
| `year_built` | number | Year of construction |
| `hoa_fee` | number (dollars) | Monthly HOA fee in dollars (0 when there is none) |
| `distance_to_center_km` | number | Distance to the city center |
| `has_pool` | yes / no | Has a pool |
| `renovated` | yes / no | Renovated in the last 10 years |

Target: `sale_price` (dollars). `year_built` is `0` when the feed did not know it.

## Part 1: Clean the data

Write `clean(df)`. It receives a raw frame exactly as `pd.read_csv` returns it (with or without the target column) and returns a cleaned **copy**:

- numeric columns stored as text become floats: strip currency symbols, thousands separators, units and percent signs
- boolean columns become `1.0` / `0.0`, whatever the spelling was
- categorical columns become lowercase, trimmed, with spaces and hyphens turned into underscores (`"Heat Pump"` and `" heat-pump "` become `heat_pump`), in the pandas `category` dtype
- every kind of missing value, and every fake "unknown" value listed above, becomes `NaN`. Do not impute and do not drop rows
- all columns stay, the index stays, the target is untouched, the input is not modified, and running it twice is safe

Every feature has its own test, so you can see which column is still wrong.

## Part 2: A first model

Write `fit_predict(train, test)`. `train` is the raw training frame including `sale_price`, `test` is the raw test frame. Clean both, train anything you like
(LightGBM, scikit-learn, ...) and return a 1-D array with the predicted sale_price for every test row.
Score: R squared on the hidden labels. It must reach **0.7**, then **0.85**. Predictions must be finite, and the frames you were given must not be modified.

## Part 3: Make it solid

Reach R squared **0.89**. Then make it robust: the function must still work when `test` contains a label never seen in training and rows where
every feature is missing, and two runs must give the same predictions (set your seeds).
