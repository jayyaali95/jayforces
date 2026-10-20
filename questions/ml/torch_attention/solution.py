import math

import torch
from torch import nn


def attention(q, k, v, mask=None):
    """Scaled dot product attention. Returns (output, weights)."""
    scores = q @ k.transpose(-2, -1) / math.sqrt(q.shape[-1])
    if mask is not None:
        scores = scores.masked_fill(~mask, float("-inf"))
    weights = torch.nan_to_num(torch.softmax(scores, dim=-1), nan=0.0)
    return weights @ v, weights


def causal_mask(L):
    """Lower triangular bool mask."""
    return torch.tril(torch.ones(L, L, dtype=torch.bool))


class MultiHeadAttention(nn.Module):
    """Multi head self attention."""

    def __init__(self, d_model, n_heads):
        super().__init__()
        if d_model % n_heads:
            raise ValueError("d_model must be divisible by n_heads")
        self.h, self.dh = n_heads, d_model // n_heads
        self.q_proj, self.k_proj = nn.Linear(d_model, d_model), nn.Linear(d_model, d_model)
        self.v_proj, self.out_proj = nn.Linear(d_model, d_model), nn.Linear(d_model, d_model)

    def forward(self, x, mask=None):
        B, L, D = x.shape
        split = lambda t: t.view(B, L, self.h, self.dh).transpose(1, 2)
        q, k, v = split(self.q_proj(x)), split(self.k_proj(x)), split(self.v_proj(x))
        if mask is not None and mask.dim() == 3:
            mask = mask.unsqueeze(1)
        out, _ = attention(q, k, v, mask)
        return self.out_proj(out.transpose(1, 2).reshape(B, L, D))
