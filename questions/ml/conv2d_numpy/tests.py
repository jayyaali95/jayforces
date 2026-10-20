import time

import numpy as np

from check import close, eq, raises

IMG = np.arange(16, dtype=float).reshape(4, 4)
K = np.array([[1.0, 0.0], [0.0, -1.0]])


def ref(img, k, s=1, p=0):
    img = np.pad(img, p)
    H, W = img.shape
    kh, kw = k.shape
    return np.array([[(img[i:i + kh, j:j + kw] * k).sum() for j in range(0, W - kw + 1, s)] for i in range(0, H - kh + 1, s)])


def test_p1_basic(sol):
    close(sol.conv2d(IMG, K), np.full((3, 3), -5.0))


def test_p1_no_flip(sol):
    k = np.array([[0.0, 1.0], [0.0, 0.0]])
    close(sol.conv2d(IMG, k)[0, 0], 1.0)


def test_p1_stride(sol):
    close(sol.conv2d(IMG, np.ones((2, 2)), stride=2), ref(IMG, np.ones((2, 2)), 2))


def test_p1_padding(sol):
    close(sol.conv2d(IMG, np.ones((3, 3)), padding=1), ref(IMG, np.ones((3, 3)), 1, 1))


def test_p1_shape_formula(sol):
    eq(sol.conv2d(np.zeros((7, 9)), np.zeros((3, 2)), stride=2, padding=1).shape, ((7 + 2 - 3) // 2 + 1, (9 + 2 - 2) // 2 + 1))


def test_p1_random(sol):
    r = np.random.default_rng(0)
    img, k = r.normal(size=(9, 11)), r.normal(size=(3, 4))
    close(sol.conv2d(img, k, 2, 1), ref(img, k, 2, 1))


def test_p1_kernel_too_big(sol):
    raises(ValueError, sol.conv2d, np.zeros((2, 2)), np.zeros((3, 3)))


def ref_batch(x, w, b, s, p):
    N, F = x.shape[0], w.shape[0]
    return np.array([[sum(ref(x[n, c], w[f, c], s, p) for c in range(x.shape[1])) + b[f] for f in range(F)] for n in range(N)])


R = np.random.default_rng(1)
XB, WB, BB = R.normal(size=(2, 3, 6, 7)), R.normal(size=(4, 3, 3, 3)), R.normal(size=4)


def test_p2_batch_shape(sol):
    eq(sol.conv2d_batch(XB, WB, BB).shape, (2, 4, 4, 5))


def test_p2_batch_values(sol):
    close(sol.conv2d_batch(XB, WB, BB), ref_batch(XB, WB, BB, 1, 0))


def test_p2_batch_stride_padding(sol):
    close(sol.conv2d_batch(XB, WB, BB, 2, 1), ref_batch(XB, WB, BB, 2, 1))


def test_p2_bias_only(sol):
    close(sol.conv2d_batch(np.zeros((1, 3, 4, 4)), np.zeros((2, 3, 2, 2)), np.array([1.0, -2.0]))[0, :, 0, 0], np.array([1.0, -2.0]))


def test_p2_batch_fast(sol):
    x, w = np.random.default_rng(0).normal(size=(16, 8, 32, 32)), np.random.default_rng(1).normal(size=(16, 8, 3, 3))
    t0 = time.perf_counter()
    sol.conv2d_batch(x, w, np.zeros(16), padding=1)
    eq(time.perf_counter() - t0 < 3, True)


def test_p2_pool(sol):
    x = np.arange(16, dtype=float).reshape(1, 1, 4, 4)
    close(sol.max_pool2d(x, 2), np.array([[[[5.0, 7.0], [13.0, 15.0]]]]))


def test_p2_pool_drops_partial(sol):
    eq(sol.max_pool2d(np.zeros((2, 3, 5, 5)), 2).shape, (2, 3, 2, 2))


def test_p2_pool_stride(sol):
    x = np.arange(16, dtype=float).reshape(1, 1, 4, 4)
    close(sol.max_pool2d(x, 2, 1), np.array([[[[5.0, 6, 7], [9, 10, 11], [13, 14, 15]]]]))
