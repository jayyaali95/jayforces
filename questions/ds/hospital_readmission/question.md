---
title: Hospital readmission
difficulty: hard
category: ds
kind: notebook
tags: healthcare, classification, noisy
timeout: 90
---
A hospital network wants to flag patients likely to come back within 30 days of discharge so care managers can arrange follow-ups. Records are merged from several clinical systems, and labs are often missing. This is a noisy problem, so expect modest scores. Predict `readmitted_30d` for the discharges in `test.csv`.

Work in the notebook on the right. It has `train.csv` (with the target) and `test.csv` (features only, the labels are hidden), and
the environment has pandas, numpy, scikit-learn and LightGBM ready. The data was generated at random for this attempt and is
**deliberately messy**: numbers stored as text, booleans written many ways, inconsistent labels, several spellings of missing, and some
fake values. Trust `info()`, `value_counts()` and your eyes, not the data dictionary alone.

| feature | type | meaning |
|---|---|---|
| `admission_type` | category | Emergency, urgent or elective |
| `diagnosis_group` | category | Primary diagnosis group |
| `discharge_to` | category | Where the patient went after discharge |
| `insurance` | category | Insurance type |
| `age_band` | category | Age bucket |
| `a1c_result` | category | HbA1c test outcome (`not_tested` is a real value) |
| `specialty` | category | Admitting specialty |
| `days_in_hospital` | number | Length of stay in days |
| `num_lab_procedures` | number | Lab procedures during the stay |
| `num_medications` | number | Distinct medications given |
| `prior_inpatient_12m` | number | Inpatient stays in the previous 12 months |
| `creatinine` | number | Serum creatinine in mg/dL |
| `followup_scheduled` | yes / no | A follow-up visit was scheduled |
| `on_insulin` | yes / no | Patient is on insulin |
| `is_icu_stay` | yes / no | Stay included intensive care |

Target: `readmitted_30d` (1 = readmitted within 30 days). `creatinine` is `-1` when the lab was not run, and `prior_inpatient_12m` is `99` when the history was unavailable.

## Part 1: Clean the data

Write `clean(df)`. It receives a raw frame exactly as `pd.read_csv` returns it (with or without the target column) and returns a cleaned **copy**:

- numeric columns stored as text become floats: strip currency symbols, thousands separators, units and percent signs
- boolean columns become `1.0` / `0.0`, whatever the spelling was
- categorical columns become lowercase, trimmed, with spaces and hyphens turned into underscores (`"Heat Pump"` and `" heat-pump "` become `heat_pump`), in the pandas `category` dtype
- every kind of missing value, and every fake "unknown" value listed above, becomes `NaN`. Do not impute and do not drop rows
- all columns stay, the index stays, the target is untouched, the input is not modified, and running it twice is safe

Every feature has its own test, so you can see which column is still wrong.

## Part 2: A first model

Write `fit_predict(train, test)`. `train` is the raw training frame including `readmitted_30d`, `test` is the raw test frame. Clean both, train anything you like
(LightGBM, scikit-learn, ...) and return a 1-D array with the predicted probability of class 1 for every test row.
Score: ROC AUC on the hidden labels. It must reach **0.62**, then **0.68**. Predictions must be finite and between 0 and 1, and the frames you were given must not be modified.

## Part 3: Make it solid

Reach ROC AUC **0.72**. Then make it robust: the function must still work when `test` contains a label never seen in training and rows where
every feature is missing, and two runs must give the same predictions (set your seeds).
