import numpy as np


def softmax(z):
    """Row wise softmax."""
    z = np.asarray(z, dtype=float)
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def log_softmax(z):
    """Row wise log softmax via log-sum-exp."""
    z = np.asarray(z, dtype=float)
    shifted = z - z.max(axis=1, keepdims=True)
    return shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))


def cross_entropy(logits, targets):
    """Mean negative log likelihood."""
    lp = log_softmax(logits)
    return float(-lp[np.arange(len(lp)), np.asarray(targets)].mean())


def cross_entropy_grad(logits, targets):
    """d(mean CE) / d(logits)."""
    p = softmax(logits)
    p[np.arange(len(p)), np.asarray(targets)] -= 1
    return p / len(p)
