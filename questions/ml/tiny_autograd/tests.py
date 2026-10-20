import math

from check import close, eq


def test_p1_add_mul(sol):
    V = sol.Value
    eq(((V(2) + V(3)).data, (V(2) * V(3)).data), (5.0, 6.0))


def test_p1_reflected(sol):
    a = sol.Value(4)
    close([(2 * a).data, (1 + a).data, (3 - a).data, (1 / a).data], [8.0, 5.0, -1.0, 0.25])


def test_p1_sub_div_neg_pow(sol):
    a, b = sol.Value(6), sol.Value(3)
    close([(a - b).data, (a / b).data, (-a).data, (a ** 2).data, (b ** 0.5).data], [3.0, 2.0, -6.0, 36.0, 3 ** 0.5])


def test_p1_activations(sol):
    V = sol.Value
    close([V(-2).relu().data, V(2).relu().data, V(0.5).tanh().data, V(1).exp().data], [0.0, 2.0, math.tanh(0.5), math.e])


def test_p1_new_objects(sol):
    a = sol.Value(1)
    b = a + 1
    eq((b is a, a.data), (False, 1.0))


def test_p1_grad_starts_zero(sol):
    eq(sol.Value(3).grad, 0.0)


def test_p2_simple_grads(sol):
    a, b = sol.Value(2), sol.Value(-3)
    (a * b + a).backward()
    close((a.grad, b.grad), (-2.0, 2.0))


def test_p2_reuse(sol):
    a = sol.Value(3)
    (a * a).backward()
    close(a.grad, 6.0)


def test_p2_shared_subexpression(sol):
    a = sol.Value(2)
    b = a * 3
    (b * b + b).backward()
    close(a.grad, (2 * 6 + 1) * 3)


def test_p2_div_pow(sol):
    a, b = sol.Value(2), sol.Value(4)
    (a / b + a ** 3).backward()
    close((a.grad, b.grad), (1 / 4 + 12, -2 / 16))


def test_p2_tanh_exp(sol):
    a = sol.Value(0.3)
    (a.tanh() * a.exp()).backward()
    t, e = math.tanh(0.3), math.exp(0.3)
    close(a.grad, (1 - t * t) * e + t * e)


def test_p2_relu_grad(sol):
    a, b = sol.Value(-1), sol.Value(2)
    (a.relu() + b.relu()).backward()
    close((a.grad, b.grad), (0.0, 1.0))


def test_p2_neuron(sol):
    V = sol.Value
    x1, x2, w1, w2, b = V(2), V(0), V(-3), V(1), V(6.881373587)
    o = (x1 * w1 + x2 * w2 + b).tanh()
    o.backward()
    close([x1.grad, w1.grad, x2.grad, w2.grad], [-1.5, 1.0, 0.5, 0.0], tol=1e-4)


def test_p2_deep_chain(sol):
    a = sol.Value(1.0)
    x = a
    for _ in range(10000):
        x = x * 1.0 + 0.0
    x.backward()
    close(a.grad, 1.0)


def test_p2_zero_grad(sol):
    a = sol.Value(2)
    out = a * a + a
    out.backward()
    out.zero_grad()
    eq((a.grad, out.grad), (0.0, 0.0))


def test_p2_numeric_check(sol):
    def f(x, y):
        X, Y = sol.Value(x), sol.Value(y)
        return X, Y, ((X * Y).tanh() + (X - Y) ** 2 / (1 + Y.exp()))
    X, Y, out = f(0.7, -0.4)
    out.backward()
    h = 1e-6
    nx = (f(0.7 + h, -0.4)[2].data - f(0.7 - h, -0.4)[2].data) / (2 * h)
    ny = (f(0.7, -0.4 + h)[2].data - f(0.7, -0.4 - h)[2].data) / (2 * h)
    close((X.grad, Y.grad), (nx, ny), tol=1e-5)
