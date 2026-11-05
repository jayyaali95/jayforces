---
title: Ad click prediction
difficulty: hard
category: ds
kind: notebook
tags: adtech, ctr, high cardinality
timeout: 90
---
An ad exchange predicts the click probability of every impression to price bids. Clicks are rare (about 5%), one column has 25 different publishers, and the logs come from several SDK versions. Predict `clicked` for the impressions in `test.csv`.

Work in the notebook on the right. It has `train.csv` (with the target) and `test.csv` (features only, the labels are hidden), and
the environment has pandas, numpy, scikit-learn and LightGBM ready. The data was generated at random for this attempt and is
**deliberately messy**: numbers stored as text, booleans written many ways, inconsistent labels, several spellings of missing, and some
fake values. Trust `info()`, `value_counts()` and your eyes, not the data dictionary alone.

| feature | type | meaning |
|---|---|---|
| `publisher` | category | Site or app that showed the ad (`pub_00` to `pub_24`) |
| `ad_format` | category | Creative format |
| `device_type` | category | Device class |
| `os` | category | Operating system |
| `country` | category | User country |
| `vertical` | category | Advertiser vertical |
| `placement` | category | Slot on the page |
| `connection` | category | Network type |
| `user_age` | number | Age of the user |
| `bid_cpm` | number (dollars) | Winning bid in dollars per thousand impressions |
| `past_ctr` | number (percent) | Historic click rate of this user, in percent |
| `impressions_7d` | number | Ads shown to this user in the last 7 days |
| `days_since_install` | number | Days since the app was installed |
| `is_returning_user` | yes / no | User has been seen before |
| `is_logged_in` | yes / no | User was logged in |

Target: `clicked` (1 = the ad was clicked). `user_age` is `0` and `days_since_install` is `9999` when unknown.

## Part 1: Clean the data

Write `clean(df)`. It receives a raw frame exactly as `pd.read_csv` returns it (with or without the target column) and returns a cleaned **copy**:

- numeric columns stored as text become floats: strip currency symbols, thousands separators, units and percent signs
- boolean columns become `1.0` / `0.0`, whatever the spelling was
- categorical columns become lowercase, trimmed, with spaces and hyphens turned into underscores (`"Heat Pump"` and `" heat-pump "` become `heat_pump`), in the pandas `category` dtype
- every kind of missing value, and every fake "unknown" value listed above, becomes `NaN`. Do not impute and do not drop rows
- all columns stay, the index stays, the target is untouched, the input is not modified, and running it twice is safe

Every feature has its own test, so you can see which column is still wrong.

## Part 2: A first model

Write `fit_predict(train, test)`. `train` is the raw training frame including `clicked`, `test` is the raw test frame. Clean both, train anything you like
(LightGBM, scikit-learn, ...) and return a 1-D array with the predicted probability of class 1 for every test row.
Score: ROC AUC on the hidden labels. It must reach **0.65**, then **0.72**. Predictions must be finite and between 0 and 1, and the frames you were given must not be modified.

## Part 3: Make it solid

Reach ROC AUC **0.75**. Then make it robust: the function must still work when `test` contains a label never seen in training and rows where
every feature is missing, and two runs must give the same predictions (set your seeds).
