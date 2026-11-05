---
title: Flight arrival delay
difficulty: medium
category: ds
kind: notebook
tags: airline, classification, cleaning
timeout: 90
---
An airline operations team wants to know the night before which flights will land late, so crews and gates can be shuffled. Rows join the schedule, weather and aircraft rotation feeds. Predict `arr_delayed` (1 = arrived more than 15 minutes late) for the flights in `test.csv`.

Work in the notebook on the right. It has `train.csv` (with the target) and `test.csv` (features only, the labels are hidden), and
the environment has pandas, numpy, scikit-learn and LightGBM ready. The data was generated at random for this attempt and is
**deliberately messy**: numbers stored as text, booleans written many ways, inconsistent labels, several spellings of missing, and some
fake values. Trust `info()`, `value_counts()` and your eyes, not the data dictionary alone.

| feature | type | meaning |
|---|---|---|
| `airline` | category | Operating carrier |
| `origin` | category | Origin airport code |
| `dest` | category | Destination airport code |
| `aircraft` | category | Aircraft type |
| `day_of_week` | category | Day of week |
| `dep_block` | category | Scheduled departure block |
| `season` | category | Season |
| `distance_miles` | number | Route distance in miles |
| `scheduled_minutes` | number | Scheduled block time in minutes |
| `wind_speed_kt` | number | Wind speed at the origin in knots |
| `visibility_miles` | number | Visibility at the origin in miles |
| `prior_leg_delay_min` | number | Delay of the previous flight of the same aircraft in minutes (early is negative) |
| `seats_sold_pct` | number (percent) | Share of seats sold, in percent |
| `is_holiday_period` | yes / no | Travel falls in a holiday period |
| `is_codeshare` | yes / no | Sold under a partner flight number |

Target: `arr_delayed` (1 = more than 15 minutes late). `prior_leg_delay_min` is `-999` when the rotation feed had no record.

## Part 1: Clean the data

Write `clean(df)`. It receives a raw frame exactly as `pd.read_csv` returns it (with or without the target column) and returns a cleaned **copy**:

- numeric columns stored as text become floats: strip currency symbols, thousands separators, units and percent signs
- boolean columns become `1.0` / `0.0`, whatever the spelling was
- categorical columns become lowercase, trimmed, with spaces and hyphens turned into underscores (`"Heat Pump"` and `" heat-pump "` become `heat_pump`), in the pandas `category` dtype
- every kind of missing value, and every fake "unknown" value listed above, becomes `NaN`. Do not impute and do not drop rows
- all columns stay, the index stays, the target is untouched, the input is not modified, and running it twice is safe

Every feature has its own test, so you can see which column is still wrong.

## Part 2: A first model

Write `fit_predict(train, test)`. `train` is the raw training frame including `arr_delayed`, `test` is the raw test frame. Clean both, train anything you like
(LightGBM, scikit-learn, ...) and return a 1-D array with the predicted probability of class 1 for every test row.
Score: ROC AUC on the hidden labels. It must reach **0.65**, then **0.71**. Predictions must be finite and between 0 and 1, and the frames you were given must not be modified.

## Part 3: Make it solid

Reach ROC AUC **0.74**. Then make it robust: the function must still work when `test` contains a label never seen in training and rows where
every feature is missing, and two runs must give the same predictions (set your seeds).
