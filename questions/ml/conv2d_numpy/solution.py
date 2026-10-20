import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def conv2d(image, kernel, stride=1, padding=0):
    """Single channel cross correlation."""
    x = np.pad(np.asarray(image, dtype=float), padding)
    k = np.asarray(kernel, dtype=float)
    if k.shape[0] > x.shape[0] or k.shape[1] > x.shape[1]:
        raise ValueError("kernel larger than padded image")
    win = sliding_window_view(x, k.shape)[::stride, ::stride]
    return np.einsum("ijkl,kl->ij", win, k)


def conv2d_batch(x, w, b, stride=1, padding=0):
    """(N, C, H, W) * (F, C, kh, kw) + b -> (N, F, Ho, Wo)."""
    x = np.pad(np.asarray(x, dtype=float), ((0, 0), (0, 0), (padding, padding), (padding, padding)))
    w = np.asarray(w, dtype=float)
    win = sliding_window_view(x, w.shape[2:], axis=(2, 3))[:, :, ::stride, ::stride]
    return np.einsum("nchwkl,fckl->nfhw", win, w) + np.asarray(b, dtype=float)[None, :, None, None]


def max_pool2d(x, size, stride=None):
    """Max pooling over (N, C, H, W)."""
    stride = stride or size
    win = sliding_window_view(np.asarray(x, dtype=float), (size, size), axis=(2, 3))[:, :, ::stride, ::stride]
    return win.max(axis=(-1, -2))
