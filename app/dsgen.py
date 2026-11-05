"""Random, deliberately messy datasets for the notebook questions (needs numpy + pandas).

A question's data.py describes the *clean* world:

    TARGET, TASK ("binary" | "regression"), METRIC ("auc" | "ap" | "r2"), SCORES (3 thresholds)
    KINDS     {column: kind}      kind = num | numtxt | money | pct | unit:<suffix> | bool | cat
    MISSING   {column: rate}      share of cells that go missing (default 5%)
    SENTINEL  {column: value}     fake "unknown" value written into ~4% of cells
    make(rng, n) -> DataFrame with proper dtypes (floats, bools, canonical lowercase labels) + TARGET

build() then corrupts the features: numbers become "$1,234.50" / "1,200 sqft" / "45.3%", booleans become
Y/yes/true/1, labels get random case and spacing, and missing cells turn into NaN or junk tokens like "?".
It also returns the ground truth so tests can check a cleaning function cell by cell.
"""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

N_TRAIN, N_TEST = 2500, 1500
DECIMALS = {"money": 2, "pct": 1, "unit": 0}
MISS_NUM, MISS_CAT = ["?", "--", "unknown", "not available"], ["?", "unknown", "unk", "-", "missing"]
BOOL_YES, BOOL_NO = ["Y", "yes", "True", "1", "T", "true"], ["N", "no", "False", "0", "F", "false"]


# ---------- helpers for data.py files ----------

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def cat(rng, n, probs):
    """Sample labels; probs is {label: weight}."""
    w = np.array(list(probs.values()), float)
    return rng.choice(list(probs), n, p=w / w.sum())


def eff(labels, effects):
    """Look up a numeric effect per label."""
    return pd.Series(labels).map(effects).to_numpy(float)


def flag(rng, n, p):
    return rng.random(n) < p


def bernoulli(rng, z, rate, scale=1.0):
    """0/1 outcomes from log-odds z: `scale` sharpens the signal, the intercept is tuned to hit `rate`."""
    z = scale * (np.asarray(z, float) - np.mean(z))
    lo, hi = -30.0, 30.0
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if sigmoid(z + mid).mean() < rate else (lo, mid)
    return (rng.random(len(z)) < sigmoid(z + lo)).astype(int)


# ---------- corruption ----------

def _fmt(v, rng, patterns):
    pick = rng.integers(0, len(patterns), len(v))
    return [patterns[i].format(x) for x, i in zip(v, pick)]


def _format(kind, v, rng):
    base = kind.split(":")[0]
    if base == "money":
        return _fmt(v, rng, ["${:,.2f}", "{:.2f}", "{:,.2f} USD"])
    if base == "pct":
        return _fmt(v, rng, ["{:.1f}%", "{:.1f}", "{:.1f} %"])
    if base == "unit":
        s = kind.split(":")[1]
        return _fmt(v, rng, ["{:,.0f} " + s, "{:.0f}", "{:.0f}" + s])
    if base == "bool":
        yes, no = rng.choice(BOOL_YES, len(v)), rng.choice(BOOL_NO, len(v))
        return np.where(v.to_numpy(bool), yes, no)
    if base == "cat":
        out = []
        for x, i in zip(v, rng.integers(0, 5, len(v))):
            out.append([x, x.upper(), x.replace("_", " ").title(), f"  {x} ", x.replace("_", "-")][i])
        return out
    return v.to_numpy()  # num / numtxt stay as they are


def corrupt(spec, X, rng):
    """Returns (raw, must_be_nan): raw is the messy frame, must_be_nan marks cells a good clean() turns into NaN."""
    raw, must = pd.DataFrame(index=X.index), pd.DataFrame(False, index=X.index, columns=X.columns)
    sentinel, missing = getattr(spec, "SENTINEL", {}), getattr(spec, "MISSING", {})
    for col, kind in spec.KINDS.items():
        v, n = X[col], len(X)
        if col in sentinel:
            hit = rng.random(n) < 0.04
            v = v.where(~hit, sentinel[col])
            must[col] |= hit
        vals = np.array(_format(kind, v, rng), dtype=object)
        gone = rng.random(n) < missing.get(col, 0.05)
        use_tokens = kind not in ("num",)
        tokens = MISS_CAT if kind.startswith("cat") or kind == "bool" else MISS_NUM
        as_token = gone & use_tokens & (rng.random(n) < 0.6)
        vals[gone] = np.nan
        vals[as_token] = rng.choice(tokens, as_token.sum())
        must[col] |= gone
        raw[col] = pd.to_numeric(vals, errors="coerce") if kind == "num" else vals
    return raw, must


def load_spec(qdir):
    path = Path(qdir) / "data.py"
    s = importlib.util.spec_from_file_location(f"data_{Path(qdir).name}", path)
    mod = importlib.util.module_from_spec(s)
    s.loader.exec_module(mod)
    return mod


def build(spec, seed):
    """Deterministic: same seed -> same everything. Used by the server (to write csv) and by tests (truth)."""
    rng = np.random.default_rng(seed)
    n_tr, n_te = getattr(spec, "N_TRAIN", N_TRAIN), getattr(spec, "N_TEST", N_TEST)
    full = spec.make(rng, n_tr + n_te)
    for col, kind in spec.KINDS.items():
        d = DECIMALS.get(kind.split(":")[0])
        if d is not None:
            full[col] = full[col].round(d)
    feats = list(spec.KINDS)
    X, y = full[feats], full[spec.TARGET]
    out = {"features": feats, "y_test": y.iloc[n_tr:].to_numpy()}
    for name, sl in (("train", slice(0, n_tr)), ("test", slice(n_tr, None))):
        truth = X.iloc[sl].reset_index(drop=True)
        raw, must = corrupt(spec, truth, rng)
        out[name] = {"truth": truth, "raw": raw, "must_nan": must}
    out["train"]["raw"][spec.TARGET] = y.iloc[:n_tr].reset_index(drop=True)
    return out


def write(qdir, seed, dest):
    """Write train.csv (with target), test.csv (features only) and info.json into dest."""
    spec = load_spec(qdir)
    b = build(spec, int(seed))
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    b["train"]["raw"].to_csv(dest / "train.csv", index=False)
    b["test"]["raw"].to_csv(dest / "test.csv", index=False)
    (dest / "info.json").write_text(json.dumps({"target": spec.TARGET, "task": spec.TASK, "metric": spec.METRIC}))
