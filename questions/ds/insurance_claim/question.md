---
title: Auto claim cost
difficulty: medium
category: ds
kind: notebook
tags: insurance, regression, skewed target
timeout: 90
---
An auto insurer reserves money for each claim as soon as it is reported. Each row is a reported claim joined with the policy and driver record. Predict `claim_cost`, the final cost of the claim, for the rows in `test.csv`. Costs are right skewed.

Work in the notebook on the right. It has `train.csv` (with the target) and `test.csv` (features only, the labels are hidden), and
the environment has pandas, numpy, scikit-learn and LightGBM ready. The data was generated at random for this attempt and is
**deliberately messy**: numbers stored as text, booleans written many ways, inconsistent labels, several spellings of missing, and some
fake values. Trust `info()`, `value_counts()` and your eyes, not the data dictionary alone.

| feature | type | meaning |
|---|---|---|
| `vehicle_class` | category | Vehicle class |
| `usage` | category | Primary use of the vehicle |
| `region` | category | Where the policy is based |
| `coverage` | category | Coverage level |
| `payment_plan` | category | How the premium is paid |
| `occupation` | category | Occupation group |
| `driver_age` | number | Age of the main driver |
| `vehicle_age_years` | number | Age of the vehicle in years |
| `annual_mileage` | number | Estimated yearly mileage |
| `prior_claims_3y` | number | Claims in the last 3 years |
| `premium_annual` | number (dollars) | Annual premium in dollars |
| `credit_score` | number | Credit based score |
| `has_telematics` | yes / no | Driving data device installed |
| `multi_policy` | yes / no | Customer has other policies with us |
| `garage_parked` | yes / no | Vehicle is parked in a garage |

Target: `claim_cost` (dollars). `driver_age` is `-1` and `credit_score` is `0` when the record was missing.

## Part 1: Clean the data

Write `clean(df)`. It receives a raw frame exactly as `pd.read_csv` returns it (with or without the target column) and returns a cleaned **copy**:

- numeric columns stored as text become floats: strip currency symbols, thousands separators, units and percent signs
- boolean columns become `1.0` / `0.0`, whatever the spelling was
- categorical columns become lowercase, trimmed, with spaces and hyphens turned into underscores (`"Heat Pump"` and `" heat-pump "` become `heat_pump`), in the pandas `category` dtype
- every kind of missing value, and every fake "unknown" value listed above, becomes `NaN`. Do not impute and do not drop rows
- all columns stay, the index stays, the target is untouched, the input is not modified, and running it twice is safe

Every feature has its own test, so you can see which column is still wrong.

## Part 2: A first model

Write `fit_predict(train, test)`. `train` is the raw training frame including `claim_cost`, `test` is the raw test frame. Clean both, train anything you like
(LightGBM, scikit-learn, ...) and return a 1-D array with the predicted claim_cost for every test row.
Score: R squared on the hidden labels. It must reach **0.45**, then **0.6**. Predictions must be finite, and the frames you were given must not be modified.

## Part 3: Make it solid

Reach R squared **0.68**. Then make it robust: the function must still work when `test` contains a label never seen in training and rows where
every feature is missing, and two runs must give the same predictions (set your seeds).
