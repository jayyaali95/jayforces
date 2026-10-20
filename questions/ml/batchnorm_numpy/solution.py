import numpy as np


class BatchNorm1d:
    """Batch norm over the batch axis of (N, D) inputs."""

    def __init__(self, dim, eps=1e-5, momentum=0.1):
        self.eps, self.momentum = eps, momentum
        self.gamma, self.beta = np.ones(dim), np.zeros(dim)
        self.running_mean, self.running_var = np.zeros(dim), np.ones(dim)

    def forward(self, x, training=True):
        x = np.asarray(x, dtype=float)
        if not training:
            return self.gamma * (x - self.running_mean) / np.sqrt(self.running_var + self.eps) + self.beta
        mean, var = x.mean(0), x.var(0)
        std = np.sqrt(var + self.eps)
        xhat = (x - mean) / std
        self._cache = (xhat, std)
        m = self.momentum
        self.running_mean = (1 - m) * self.running_mean + m * mean
        self.running_var = (1 - m) * self.running_var + m * x.var(0, ddof=1)
        return self.gamma * xhat + self.beta

    def backward(self, dout):
        xhat, std = self._cache
        n = len(dout)
        dgamma, dbeta = (dout * xhat).sum(0), dout.sum(0)
        dxhat = dout * self.gamma
        dx = (n * dxhat - dxhat.sum(0) - xhat * (dxhat * xhat).sum(0)) / (n * std)
        return dx, dgamma, dbeta
