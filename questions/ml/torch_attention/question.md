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

## Part 2: Multi head attention

Implement `class MultiHeadAttention(nn.Module)` with `__init__(self, d_model, n_heads)` (raise `ValueError` if `d_model % n_heads`)
and four layers named exactly `q_proj`, `k_proj`, `v_proj`, `out_proj`, each `nn.Linear(d_model, d_model)`.
`forward(x, mask=None)` takes `x (B, L, d_model)`, projects, splits into heads `(B, n_heads, L, d_model // n_heads)`, applies
`attention` (a mask of shape `(L, L)` or `(B, L, L)` must work), merges heads back and applies `out_proj`. Return only the output.
