import numpy as np


def init_params(d, h, k, seed=0):
    """He initialized weights, zero biases."""
    rng = np.random.default_rng(seed)
    W1 = rng.normal(size=(d, h)) * np.sqrt(2 / d)
    W2 = rng.normal(size=(h, k)) * np.sqrt(2 / h)
    return {"W1": W1, "b1": np.zeros(h), "W2": W2, "b2": np.zeros(k)}


def forward(params, X):
    """Return logits and what backward needs."""
    z1 = X @ params["W1"] + params["b1"]
    a1 = np.maximum(z1, 0)
    return a1 @ params["W2"] + params["b2"], (X, z1, a1)


def _probs(logits):
    e = np.exp(logits - logits.max(1, keepdims=True))
    return e / e.sum(1, keepdims=True)


def loss(params, X, y):
    """Mean cross entropy."""
    logits, _ = forward(params, X)
    s = logits - logits.max(1, keepdims=True)
    lp = s - np.log(np.exp(s).sum(1, keepdims=True))
    return float(-lp[np.arange(len(y)), y].mean())


def backward(params, X, y):
    """Gradients of the mean loss."""
    logits, (X, z1, a1) = forward(params, X)
    d = _probs(logits)
    d[np.arange(len(y)), y] -= 1
    d /= len(y)
    dz1 = (d @ params["W2"].T) * (z1 > 0)
    return {"W2": a1.T @ d, "b2": d.sum(0), "W1": X.T @ dz1, "b1": dz1.sum(0)}


def train(X, y, h=16, lr=0.5, epochs=300, seed=0):
    """Full batch gradient descent."""
    params = init_params(X.shape[1], h, int(y.max()) + 1, seed)
    losses = []
    for _ in range(epochs):
        losses.append(loss(params, X, y))
        g = backward(params, X, y)
        params = {k: v - lr * g[k] for k, v in params.items()}
    return params, losses
