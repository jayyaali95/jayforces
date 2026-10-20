import numpy as np


def zscore_mask(x, threshold=3.0):
    """True where |z| > threshold."""
    x = np.asarray(x, dtype=float)
    std = x.std()
    if std == 0:
        return np.zeros(len(x), dtype=bool)
    return np.abs(x - x.mean()) / std > threshold


def iqr_mask(x, k=1.5):
    """True outside the Tukey fences."""
    x = np.asarray(x, dtype=float)
    q1, q3 = np.percentile(x, [25, 75])
    iqr = q3 - q1
    return (x < q1 - k * iqr) | (x > q3 + k * iqr)


def mad_mask(x, threshold=3.5):
    """Modified z score using the median absolute deviation."""
    x = np.asarray(x, dtype=float)
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    if mad == 0:
        return x != med
    return np.abs(0.6745 * (x - med) / mad) > threshold


def group_iqr_mask(values, groups, k=1.5):
    """IQR outliers computed within each group."""
    values, groups = np.asarray(values, dtype=float), np.asarray(groups)
    out = np.zeros(len(values), dtype=bool)
    for g in np.unique(groups):
        m = groups == g
        out[m] = iqr_mask(values[m], k)
    return out
