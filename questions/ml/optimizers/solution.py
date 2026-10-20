import numpy as np


class SGD:
    """Stochastic gradient descent with optional momentum and L2."""

    def __init__(self, lr, momentum=0.0, weight_decay=0.0):
        self.lr, self.momentum, self.wd = lr, momentum, weight_decay
        self.buf = {}

    def step(self, params, grads):
        for k, p in params.items():
            g = grads[k] + self.wd * p
            if self.momentum:
                self.buf[k] = g.copy() if k not in self.buf else self.momentum * self.buf[k] + g
                g = self.buf[k]
            p -= self.lr * g


class Adam:
    """Adam with bias correction and optional L2."""

    def __init__(self, lr=1e-3, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0):
        self.lr, (self.b1, self.b2), self.eps, self.wd = lr, betas, eps, weight_decay
        self.m, self.v, self.t = {}, {}, {}

    def step(self, params, grads):
        for k, p in params.items():
            g = grads[k] + self.wd * p
            self.t[k] = t = self.t.get(k, 0) + 1
            self.m[k] = self.b1 * self.m.get(k, 0) + (1 - self.b1) * g
            self.v[k] = self.b2 * self.v.get(k, 0) + (1 - self.b2) * g * g
            m_hat = self.m[k] / (1 - self.b1 ** t)
            v_hat = self.v[k] / (1 - self.b2 ** t)
            p -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)


def minimize(grad_fn, x0, opt, steps):
    """Run an optimizer on a single array."""
    params = {"x": np.array(x0, dtype=float)}
    for _ in range(steps):
        opt.step(params, {"x": grad_fn(params["x"])})
    return params["x"]
