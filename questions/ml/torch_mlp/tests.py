import torch
from torch import nn

from check import eq


def blobs():
    g = torch.Generator().manual_seed(0)
    X = torch.cat([torch.randn(100, 2, generator=g) + 3, torch.randn(100, 2, generator=g) - 3])
    y = torch.cat([torch.zeros(100), torch.ones(100)]).long()
    return X, y


def model(sol, *a, **kw):
    torch.manual_seed(0)
    return sol.MLP(*a, **kw)


def test_p1_is_module(sol):
    eq(isinstance(model(sol, 4, [8], 2), nn.Module), True)


def test_p1_output_shape(sol):
    eq(tuple(model(sol, 4, [16, 8], 3)(torch.randn(5, 4)).shape), (5, 3))


def test_p1_linear_shapes(sol):
    m = model(sol, 4, [16, 8], 3)
    eq([tuple(l.weight.shape) for l in m.modules() if isinstance(l, nn.Linear)], [(16, 4), (8, 16), (3, 8)])


def test_p1_relu_count(sol):
    eq(sum(isinstance(l, nn.ReLU) for l in model(sol, 4, [16, 8], 3).modules()), 2)


def test_p1_no_dropout_by_default(sol):
    eq(sum(isinstance(l, nn.Dropout) for l in model(sol, 4, [16, 8], 3).modules()), 0)


def test_p1_dropout_layers(sol):
    eq(sum(isinstance(l, nn.Dropout) for l in model(sol, 4, [16, 8], 3, dropout=0.5).modules()), 2)


def test_p1_eval_deterministic(sol):
    m = model(sol, 4, [32], 2, dropout=0.5).eval()
    x = torch.randn(3, 4)
    eq(torch.equal(m(x), m(x)), True)


def test_p1_count_params(sol):
    eq(sol.count_params(model(sol, 4, [16, 8], 3)), 4 * 16 + 16 + 16 * 8 + 8 + 8 * 3 + 3)


def test_p1_count_trainable_only(sol):
    m = model(sol, 4, [16, 8], 3)
    first = next(l for l in m.modules() if isinstance(l, nn.Linear))
    first.weight.requires_grad_(False)
    eq(sol.count_params(m), 243 - 64)


def test_p1_no_hidden(sol):
    m = model(sol, 4, [], 3)
    eq((sol.count_params(m), tuple(m(torch.randn(2, 4)).shape)), (15, (2, 3)))


def test_p1_gradients_flow(sol):
    m = model(sol, 4, [8, 8], 2)
    m(torch.randn(6, 4)).sum().backward()
    eq(all(p.grad is not None for p in m.parameters()), True)


def test_p2_loss_list(sol):
    X, y = blobs()
    losses = sol.train(model(sol, 2, [8], 2), X, y, epochs=5)
    eq((len(losses), all(type(l) is float for l in losses)), (5, True))


def test_p2_loss_goes_down(sol):
    X, y = blobs()
    losses = sol.train(model(sol, 2, [16], 2), X, y, epochs=20)
    eq(losses[-1] < losses[0] * 0.5, True, msg=f"first {losses[0]:.3f}, last {losses[-1]:.3f}")


def test_p2_learns(sol):
    X, y = blobs()
    m = model(sol, 2, [16], 2)
    sol.train(m, X, y, epochs=30)
    eq(sol.accuracy(m, X, y) > 0.95, True)


def test_p2_reproducible(sol):
    X, y = blobs()
    a = sol.train(model(sol, 2, [8], 2), X, y, epochs=3, seed=1)
    b = sol.train(model(sol, 2, [8], 2), X, y, epochs=3, seed=1)
    eq(a, b)


def test_p2_accuracy_float_range(sol):
    X, y = blobs()
    a = sol.accuracy(model(sol, 2, [8], 2), X, y)
    eq((type(a) is float, 0.0 <= a <= 1.0), (True, True))


def test_p2_accuracy_keeps_mode(sol):
    X, y = blobs()
    m = model(sol, 2, [8], 2, dropout=0.2)
    m.train()
    sol.accuracy(m, X, y)
    eq(m.training, True)


def test_p2_accuracy_keeps_eval_mode(sol):
    X, y = blobs()
    m = model(sol, 2, [8], 2).eval()
    sol.accuracy(m, X, y)
    eq(m.training, False)


def test_p2_accuracy_no_grad(sol):
    X, y = blobs()
    m = model(sol, 2, [8], 2)
    sol.accuracy(m, X, y)
    eq(all(p.grad is None for p in m.parameters()), True)
