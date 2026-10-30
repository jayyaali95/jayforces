---
title: Attention in PyTorch
difficulty: hard
category: ml
tags: pytorch, transformers, masking
timeout: 30
---
Implement attention the way a transformer layer uses it. Do not call `torch.nn.functional.scaled_dot_product_attention` or `nn.MultiheadAttention`.

## Part 1: Scaled dot product attention

Implement `attention(q, k, v, mask=None)` for `q (..., Lq, d)`, `k (..., Lk, d)`, `v (..., Lk, dv)`. Scores are
`q @ k^T / sqrt(d)`. `mask` is a bool tensor broadcastable to `(..., Lq, Lk)` where `True` means "may attend"; disallowed scores
become `-inf` before the softmax. A query row with nothing allowed gets all zero weights (never `nan`). Return `(output, weights)`.

Implement `causal_mask(L)` returning a bool `(L, L)` tensor where position `i` may attend to positions `<= i`.

**Example**
```python
>>> q = k = torch.tensor([[1., 0.], [0., 1.]])
>>> v = torch.tensor([[1., 2.], [3., 4.]])
>>> out, weights = attention(q, k, v)   # rounded to 4 decimals
>>> out
tensor([[1.6605, 2.6605],
        [2.3395, 3.3395]])
>>> weights
tensor([[0.6698, 0.3302],
        [0.3302, 0.6698]])
>>> causal_mask(3)
tensor([[ True, False, False],
        [ True,  True, False],
        [ True,  True,  True]])
>>> out, weights = attention(q, k, v, causal_mask(2))   # row 0 can only see position 0
>>> weights
tensor([[1.0000, 0.0000],
        [0.3302, 0.6698]])
>>> attention(q, k, v, torch.tensor([[True, True], [False, False]]))[1]   # fully masked row -> zeros, not nan
tensor([[0.6698, 0.3302],
        [0.0000, 0.0000]])
```

## Part 2: Multi head attention

Implement `class MultiHeadAttention(nn.Module)` with `__init__(self, d_model, n_heads)` (raise `ValueError` if `d_model % n_heads`)
and four layers named exactly `q_proj`, `k_proj`, `v_proj`, `out_proj`, each `nn.Linear(d_model, d_model)`.
`forward(x, mask=None)` takes `x (B, L, d_model)`, projects, splits into heads `(B, n_heads, L, d_model // n_heads)`, applies
`attention` (a mask of shape `(L, L)` or `(B, L, L)` must work), merges heads back and applies `out_proj`. Return only the output.

**Example**
```python
>>> mha = MultiHeadAttention(d_model=8, n_heads=2)
>>> x = torch.randn(2, 5, 8)
>>> mha(x, causal_mask(5)).shape   # (L, L) mask; a (B, L, L) mask works too
torch.Size([2, 5, 8])
>>> MultiHeadAttention(6, 4)
ValueError: d_model must be divisible by n_heads
```
