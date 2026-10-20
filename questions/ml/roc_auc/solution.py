import numpy as np


def _avg_ranks(x):
    order = np.argsort(x, kind="mergesort")
    xs = x[order]
    ranks = np.empty(len(x))
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and xs[j + 1] == xs[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def roc_auc(y, scores):
    """AUC via the rank sum statistic."""
    y, s = np.asarray(y), np.asarray(scores, dtype=float)
    pos, neg = int((y == 1).sum()), int((y == 0).sum())
    if pos == 0 or neg == 0:
        raise ValueError("need both classes")
    r = _avg_ranks(s)
    return float((r[y == 1].sum() - pos * (pos + 1) / 2) / (pos * neg))


def roc_curve(y, scores):
    """False positive rate, true positive rate and thresholds."""
    y, s = np.asarray(y), np.asarray(scores, dtype=float)
    th = np.concatenate([[np.inf], np.unique(s)[::-1]])
    pred = s[None, :] >= th[:, None]
    tpr = (pred & (y == 1)).sum(1) / (y == 1).sum()
    fpr = (pred & (y == 0)).sum(1) / (y == 0).sum()
    return fpr, tpr, th


def auc_trapezoid(fpr, tpr):
    """Area under a curve given by points."""
    fpr, tpr = np.asarray(fpr, dtype=float), np.asarray(tpr, dtype=float)
    return float(np.sum(np.diff(fpr) * (tpr[1:] + tpr[:-1]) / 2))
