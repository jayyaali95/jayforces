import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

TARGET = "readmitted_30d"
_cats = ['admission_type', 'diagnosis_group', 'discharge_to', 'insurance', 'age_band', 'a1c_result', 'specialty']
_nums = ['days_in_hospital', 'num_lab_procedures', 'num_medications', 'prior_inpatient_12m', 'creatinine']
_bools = ['followup_scheduled', 'on_insulin', 'is_icu_stay']
_missing = {"nan", "?", "unknown", "unk", "-", "--", "missing", "not available"}
_yes = {"y", "yes", "true", "t", "1", "1.0"}
_no = {"n", "no", "false", "f", "0", "0.0"}


def clean(df):
    """Return a cleaned copy of df.

    Numbers become floats, booleans become 1.0 / 0.0, categories become lowercase_with_underscores in the
    `category` dtype. Every kind of missing, and every fake "unknown" value, becomes NaN. Do not impute.
    The target column, if present, is left alone.
    """
    out = df.copy()
    for c in _nums:
        out[c] = pd.to_numeric(out[c].astype(str).str.replace(r"[^0-9.\-]", "", regex=True), errors="coerce")
    out.loc[out["creatinine"] == -1, "creatinine"] = np.nan
    out.loc[out["prior_inpatient_12m"] == 99, "prior_inpatient_12m"] = np.nan
    for c in _bools:
        s = out[c].astype(str).str.strip().str.lower()
        out[c] = s.map(lambda x: 1.0 if x in _yes else 0.0 if x in _no else np.nan)
    for c in _cats:
        s = out[c].astype(str).str.strip().str.lower()
        out[c] = s.mask(s.isin(_missing)).str.replace(r"[\s-]+", "_", regex=True).astype("category")
    return out


def fit_predict(train, test):
    """Train on `train` (it still has the target column) and return predictions for every row of `test`."""
    X = clean(train.drop(columns=TARGET))
    model = HistGradientBoostingClassifier(max_iter=120, learning_rate=0.04, max_leaf_nodes=8, l2_regularization=2.0, categorical_features="from_dtype", random_state=0)
    model.fit(X, train[TARGET])
    Xt = clean(test)[X.columns]
    return model.predict_proba(Xt)[:, 1]
