"""Test factory for the notebook questions. A notebook question's tests.py is just:

    from dscheck import suite
    suite(globals())

Part 1 checks `clean(df)` column by column against the ground truth that dsgen kept.
Part 2 checks `fit_predict(train, test)` shape, validity and a first score threshold.
Part 3 checks the strong score threshold, robustness to unseen labels and empty rows, determinism.
"""
import os
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype

import dsgen


def suite(g):
    spec = dsgen.load_spec(Path(g["__file__"]).parent)
    b = dsgen.build(spec, int(os.environ.get("JF_SEED", 7)))
    feats, target = b["features"], spec.TARGET
    raw = {"train": pd.read_csv("train.csv"), "test": pd.read_csv("test.csv")}  # exactly what the notebook sees
    memo = {}

    def once(key, fn):  # run expensive things (training!) once per run, remember failures too
        if key not in memo:
            try:
                memo[key] = (fn(), None)
            except BaseException as e:
                memo[key] = (None, e)
        value, err = memo[key]
        if err is not None:
            raise err
        return value

    def add(part, name, fn):
        key = f"test_p{part}_{name}"
        fn.__name__ = key
        g[key] = fn

    def cleaned(sol, which="train"):
        return once(("clean", which), lambda: sol.clean(raw[which].copy()))

    # ---------- part 1: clean() ----------

    def column_problem(out, which, col):
        """None if `out[col]` matches the ground truth, else a message."""
        if col not in out.columns:
            return f"{col}: column is missing from the result"
        s, kind = out[col], spec.KINDS[col].split(":")[0]
        truth, must = b[which]["truth"][col], b[which]["must_nan"][col].to_numpy()
        n = min(len(s), len(truth))
        if kind == "cat":
            if not isinstance(s.dtype, pd.CategoricalDtype):
                return f"{col}: expected the pandas 'category' dtype, got {s.dtype}"
            got, exp = np.asarray(s.astype(object)), truth.to_numpy(dtype=object)
            same = np.array([a == e for a, e in zip(got, exp)])
        else:
            if kind != "bool" and (not is_numeric_dtype(s) or is_bool_dtype(s)):
                return f"{col}: expected a numeric dtype, got {s.dtype}"
            try:
                got = s.to_numpy(dtype=float, na_value=np.nan)
            except (TypeError, ValueError):
                return f"{col}: could not read the values as numbers (dtype {s.dtype})"
            exp = truth.to_numpy(dtype=float)
            same = np.isclose(got, exp, rtol=1e-6, atol=1e-6)
        gone = np.asarray(s.isna())
        bad = np.flatnonzero((gone != must[:n]) | (~must[:n] & ~same[:n] & ~gone))
        if len(bad) == 0:
            return None
        i = bad[0]
        want = "NaN" if must[i] else repr(exp[i].item() if hasattr(exp[i], "item") else exp[i])
        found = s.iloc[i].item() if hasattr(s.iloc[i], "item") else s.iloc[i]
        return f"{col}: {len(bad)} wrong cells, first at row {i}: expected {want}, got {found!r} (raw value {raw_of(which, col, i)!r})"

    def raw_of(which, col, i):
        return raw[which][col].iloc[i] if len(raw[which]) > i else None

    def all_problems(out, which="train"):
        return [m for m in (column_problem(out, which, c) for c in feats) if m]

    def t_frame(sol):
        out = cleaned(sol)
        assert isinstance(out, pd.DataFrame), f"clean() must return a DataFrame, got {type(out).__name__}"
        assert len(out) == len(raw["train"]), f"expected {len(raw['train'])} rows, got {len(out)}: clean() should not drop rows"
        assert out.index.equals(raw["train"].index), "the index must be left as it was"

    def t_no_mutation(sol):
        df = raw["train"].copy()
        before = df.copy(deep=True)
        sol.clean(df)
        assert df.equals(before), "clean() changed its input DataFrame, work on a copy"

    def t_columns(sol):
        out = cleaned(sol)
        assert set(out.columns) == set(raw["train"].columns), \
            f"columns differ. missing: {sorted(set(raw['train'].columns) - set(out.columns))}, extra: {sorted(set(out.columns) - set(raw['train'].columns))}"
        assert out[target].equals(raw["train"][target]), f"the target column '{target}' must pass through untouched"

    def t_dtypes(sol):
        out = cleaned(sol)
        bad = [f"{c} ({out[c].dtype})" for c in feats if c in out
               and not (isinstance(out[c].dtype, pd.CategoricalDtype) or is_numeric_dtype(out[c]) or is_bool_dtype(out[c]))]
        assert not bad, "still not numeric/bool/category: " + ", ".join(bad)

    def t_test_frame(sol):
        out = sol.clean(raw["test"].copy())
        assert list(out.columns) == list(raw["test"].columns), "clean() must also work on a frame without the target column"
        bad = all_problems(out, "test")
        assert not bad, f"{len(bad)} columns wrong on the test frame. " + bad[0]

    def t_idempotent(sol):
        bad = all_problems(sol.clean(cleaned(sol).copy()))
        assert not bad, "clean(clean(df)) is not the same as clean(df). " + (bad[0] if bad else "")

    def t_one_row(sol):
        out = sol.clean(raw["train"].head(1).copy())
        assert len(out) == 1, f"expected 1 row, got {len(out)}"

    add(1, "returns_a_dataframe_with_the_same_rows", t_frame)
    add(1, "does_not_modify_its_input", t_no_mutation)
    add(1, "keeps_every_column_and_the_target", t_columns)
    add(1, "leaves_no_object_columns", t_dtypes)
    for col in feats:
        add(1, f"column_{col}", lambda sol, col=col: _fail(column_problem(cleaned(sol), "train", col)))
    add(1, "cleans_a_frame_without_the_target", t_test_frame)
    add(1, "is_safe_to_run_twice", t_idempotent)
    add(1, "handles_a_single_row", t_one_row)

    # ---------- part 2 and 3: fit_predict() ----------

    def metric(y, p):
        from sklearn import metrics
        return {"auc": metrics.roc_auc_score, "ap": metrics.average_precision_score, "r2": metrics.r2_score}[spec.METRIC](y, p)

    def base(sol):
        def go():
            tr, te = raw["train"].copy(), raw["test"].copy()
            tr0, te0 = tr.copy(deep=True), te.copy(deep=True)
            p = np.asarray(sol.fit_predict(tr, te))
            return p, tr.equals(tr0) and te.equals(te0)
        return once("base", go)

    def preds(sol):
        p = base(sol)[0]
        assert p.shape == (len(raw["test"]),), f"expected a 1-D array of {len(raw['test'])} predictions, got shape {p.shape}"
        return p.astype(float)

    def t_shape(sol):
        preds(sol)

    def t_finite(sol):
        assert np.isfinite(preds(sol)).all(), "some predictions are NaN or infinite"

    def t_range(sol):
        p, y = preds(sol), raw["train"][target]
        if spec.TASK == "binary":
            assert ((p >= 0) & (p <= 1)).all(), "return the probability of class 1, every value must be in [0, 1]"
        else:
            span = y.max() - y.min()
            assert ((p > y.min() - span) & (p < y.max() + span)).all(), "some predictions are far outside the range of the target"
        assert np.ptp(p) > 0, "every prediction is identical"

    def t_untouched(sol):
        assert base(sol)[1], "fit_predict() changed the DataFrames you passed in, work on copies"

    def t_score(threshold):
        def test(sol):
            s = metric(b["y_test"], preds(sol))
            assert s >= threshold, f"{spec.METRIC} on the hidden test set is {s:.3f}, need {threshold}"
        return test

    def t_messy(sol):
        te = raw["test"].copy()
        first_cat = next(c for c in feats if spec.KINDS[c].startswith("cat"))
        te[first_cat] = te[first_cat].astype(object)
        te.loc[te.index[:5], first_cat] = "Brand New Label"
        for c in feats:
            te[c] = te[c].astype(object)
            te.loc[te.index[5:8], c] = np.nan
        p = np.asarray(sol.fit_predict(raw["train"].copy(), te), dtype=float)
        assert p.shape == (len(te),) and np.isfinite(p).all(), "unseen labels or all-missing rows broke the predictions"

    def t_repeatable(sol):
        again = np.asarray(sol.fit_predict(raw["train"].copy(), raw["test"].copy()), dtype=float)
        assert np.allclose(preds(sol), again, atol=1e-6), "two runs gave different predictions, fix the random seeds"

    lo, mid, high = spec.SCORES
    add(2, "returns_one_prediction_per_test_row", t_shape)
    add(2, "predictions_are_finite", t_finite)
    add(2, "predictions_are_valid", t_range)
    add(2, "does_not_modify_its_inputs", t_untouched)
    add(2, f"{spec.METRIC}_at_least_{lo}", t_score(lo))
    add(2, f"{spec.METRIC}_at_least_{mid}", t_score(mid))
    add(3, f"{spec.METRIC}_at_least_{high}", t_score(high))
    add(3, "survives_unseen_labels_and_empty_rows", t_messy)
    add(3, "is_repeatable", t_repeatable)


def _fail(msg):
    assert msg is None, msg
