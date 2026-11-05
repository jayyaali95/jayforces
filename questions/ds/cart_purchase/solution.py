import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier

TARGET = "purchased"
_cats = ['traffic_source', 'device', 'country', 'browser', 'landing_category', 'customer_segment']
_nums = ['pages_viewed', 'session_minutes', 'cart_value', 'items_in_cart', 'prior_orders']
_bools = ['is_logged_in', 'has_coupon', 'is_weekend']
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
    out.loc[out["prior_orders"] == -1, "prior_orders"] = np.nan
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
    model = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.06, max_leaf_nodes=20, l2_regularization=1.0, categorical_features="from_dtype", random_state=0)
    model.fit(X, train[TARGET])
    Xt = clean(test)[X.columns]
    return model.predict_proba(Xt)[:, 1]
