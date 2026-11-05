---
title: Delivery time estimate
difficulty: medium
category: ds
kind: notebook
tags: delivery, regression, cleaning
timeout: 90
---
A food delivery app promises an arrival time at checkout. Late deliveries cost refunds, early quotes cost orders. Each row is a finished order logged by the restaurant, courier and weather systems. Predict `delivery_minutes`, the time from order to doorstep, for the orders in `test.csv`.

Work in the notebook on the right. It has `train.csv` (with the target) and `test.csv` (features only, the labels are hidden), and
the environment has pandas, numpy, scikit-learn and LightGBM ready. The data was generated at random for this attempt and is
**deliberately messy**: numbers stored as text, booleans written many ways, inconsistent labels, several spellings of missing, and some
fake values. Trust `info()`, `value_counts()` and your eyes, not the data dictionary alone.

| feature | type | meaning |
|---|---|---|
| `cuisine` | category | Cuisine of the restaurant |
| `vehicle` | category | Courier vehicle |
| `weather` | category | Weather at pickup |
| `traffic` | category | Traffic level |
| `zone` | category | Delivery zone |
| `day_part` | category | Part of the day |
| `distance_m` | number | Route distance in meters |
| `n_items` | number | Items in the order |
| `order_value` | number (dollars) | Order value in dollars |
| `courier_rating` | number | Courier rating, 1 to 5 |
| `prep_time_min` | number | Restaurant preparation time in minutes |
| `temp_c` | number | Temperature in Celsius |
| `is_weekend` | yes / no | Order placed on a weekend |
| `is_first_order` | yes / no | Customer first order |
| `is_scheduled` | yes / no | Scheduled ahead of time |

Target: `delivery_minutes` (minutes). `courier_rating` is `0` for couriers that were not rated yet.

## Part 1: Clean the data

Write `clean(df)`. It receives a raw frame exactly as `pd.read_csv` returns it (with or without the target column) and returns a cleaned **copy**:

- numeric columns stored as text become floats: strip currency symbols, thousands separators, units and percent signs
- boolean columns become `1.0` / `0.0`, whatever the spelling was
- categorical columns become lowercase, trimmed, with spaces and hyphens turned into underscores (`"Heat Pump"` and `" heat-pump "` become `heat_pump`), in the pandas `category` dtype
- every kind of missing value, and every fake "unknown" value listed above, becomes `NaN`. Do not impute and do not drop rows
- all columns stay, the index stays, the target is untouched, the input is not modified, and running it twice is safe

Every feature has its own test, so you can see which column is still wrong.

## Part 2: A first model

Write `fit_predict(train, test)`. `train` is the raw training frame including `delivery_minutes`, `test` is the raw test frame. Clean both, train anything you like
(LightGBM, scikit-learn, ...) and return a 1-D array with the predicted delivery_minutes for every test row.
Score: R squared on the hidden labels. It must reach **0.6**, then **0.75**. Predictions must be finite, and the frames you were given must not be modified.

## Part 3: Make it solid

Reach R squared **0.8**. Then make it robust: the function must still work when `test` contains a label never seen in training and rows where
every feature is missing, and two runs must give the same predictions (set your seeds).
