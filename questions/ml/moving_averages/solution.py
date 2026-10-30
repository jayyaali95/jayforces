import numpy as np


def sma(x, window):
    """Simple moving average via cumulative sum."""
    x = np.asarray(x, dtype=float)
    if window < 1 or window > len(x):
        raise ValueError("bad window")
    c = np.concatenate([[0.0], np.cumsum(x)])
    return (c[window:] - c[:-window]) / window


def ema(x, alpha):
    """Exponential moving average."""
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    for t, v in enumerate(x):
        out[t] = v if t == 0 else alpha * v + (1 - alpha) * out[t - 1]
    return out


def rolling_zscore(x, window):
    """Z score of each point against its trailing window."""
    x = np.asarray(x, dtype=float)
    out = np.full(len(x), np.nan)
    if window > len(x):
        return out
    w = np.lib.stride_tricks.sliding_window_view(x, window)
    mean, std = w.mean(1), w.std(1)
    z = np.divide(x[window - 1:] - mean, std, out=np.zeros(len(mean)), where=std > 0)
    out[window - 1:] = z
    return out
