---
title: 2D convolution in numpy
difficulty: medium
category: ml
tags: numpy, cnn, indexing
---
Implement the core of a CNN layer. As in deep learning libraries, "convolution" here means cross correlation (no kernel flip).

## Part 1: Single channel

Implement `conv2d(image, kernel, stride=1, padding=0)` for a 2D image `(H, W)` and kernel `(kh, kw)`. Zero padding is added on
all sides. Output size is `(H + 2p - kh) // s + 1` by `(W + 2p - kw) // s + 1`. Raise `ValueError` if the kernel does not fit.

## Part 2: Batched, multi channel, pooling

Implement `conv2d_batch(x, w, b, stride=1, padding=0)` with `x` `(N, C, H, W)`, `w` `(F, C, kh, kw)`, `b` `(F,)` returning
`(N, F, Ho, Wo)`. Avoid Python loops over N, F and C (looping over output positions or kernel offsets is fine; `einsum` and
`sliding_window_view` are allowed). Implement `max_pool2d(x, size, stride=None)` on `(N, C, H, W)` where stride defaults to size and
partial windows at the edge are dropped.
