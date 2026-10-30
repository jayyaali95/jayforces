import math

import torch
from torch import nn

from check import eq


def close_t(a, b, tol=1e-4):
    eq(torch.allclose(a, b, atol=tol, rtol=tol), True, msg=f"max diff {(a - b).abs().max().item():.2e}")


torch.manual_seed(0)
Q, K, V = torch.randn(2, 3, 4), torch.randn(2, 5, 4), torch.randn(2, 5, 6)


def manual(q, k, v):
    w = torch.softmax(q @ k.transpose(-2, -1) / math.sqrt(q.shape[-1]), -1)
    return w @ v, w


def test_p1_shapes(sol):
    out, w = sol.attention(Q, K, V)
    eq((tuple(out.shape), tuple(w.shape)), ((2, 3, 6), (2, 3, 5)))


def test_p1_values(sol):
    out, w = sol.attention(Q, K, V)
    mo, mw = manual(Q, K, V)
    close_t(out, mo)
    close_t(w, mw)


def test_p1_rows_sum_to_one(sol):
    close_t(sol.attention(Q, K, V)[1].sum(-1), torch.ones(2, 3))


def test_p1_scaling(sol):
    q = torch.ones(1, 1, 64)
    k = torch.stack([torch.ones(64), torch.zeros(64)]).unsqueeze(0)
    _, w = sol.attention(q, k, torch.zeros(1, 2, 1))
    close_t(w, torch.softmax(torch.tensor([[[8.0, 0.0]]]), -1))


def test_p1_causal_mask(sol):
    eq(sol.causal_mask(3).tolist(), [[True, False, False], [True, True, False], [True, True, True]])


def test_p1_causal_mask_dtype(sol):
    eq(sol.causal_mask(4).dtype, torch.bool)


def test_p1_causal_first_position(sol):
    x = torch.randn(2, 4, 8)
    out, w = sol.attention(x, x, x, sol.causal_mask(4))
    close_t(out[:, 0], x[:, 0])
    eq(bool((w.triu(1) == 0).all()), True)


def test_p1_mask_broadcast_batch(sol):
    m = torch.tensor([[True, False, True, True, False]] * 3)
    _, w = sol.attention(Q, K, V, m)
    eq(bool((w[..., 1] == 0).all() and (w[..., 4] == 0).all()), True)


def test_p1_fully_masked_row(sol):
    m = torch.ones(3, 5, dtype=torch.bool)
    m[1] = False
    out, w = sol.attention(Q, K, V, m)
    eq((bool(torch.isnan(out).any()), w[:, 1].abs().sum().item()), (False, 0.0))


def test_p1_gradients(sol):
    q = Q.clone().requires_grad_()
    sol.attention(q, K, V)[0].sum().backward()
    eq(q.grad is not None and bool(torch.isfinite(q.grad).all()), True)


def mha(sol, d=8, h=2):
    torch.manual_seed(1)
    return sol.MultiHeadAttention(d, h)


def reference(m, d, h):
    ref = nn.MultiheadAttention(d, h, batch_first=True)
    with torch.no_grad():
        ref.in_proj_weight.copy_(torch.cat([m.q_proj.weight, m.k_proj.weight, m.v_proj.weight]))
        ref.in_proj_bias.copy_(torch.cat([m.q_proj.bias, m.k_proj.bias, m.v_proj.bias]))
        ref.out_proj.weight.copy_(m.out_proj.weight)
        ref.out_proj.bias.copy_(m.out_proj.bias)
    return ref.eval()


def test_p2_bad_heads(sol):
    try:
        sol.MultiHeadAttention(10, 3)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_p2_layers(sol):
    m = mha(sol)
    eq([tuple(getattr(m, n).weight.shape) for n in ("q_proj", "k_proj", "v_proj", "out_proj")], [(8, 8)] * 4)


def test_p2_output_shape(sol):
    eq(tuple(mha(sol)(torch.randn(3, 5, 8)).shape), (3, 5, 8))


def test_p2_param_count(sol):
    eq(sum(p.numel() for p in mha(sol).parameters()), 4 * (64 + 8))


def test_p2_matches_torch(sol):
    m, x = mha(sol), torch.randn(2, 5, 8)
    with torch.no_grad():
        close_t(m(x), reference(m, 8, 2)(x, x, x, need_weights=False)[0])


def test_p2_matches_torch_causal(sol):
    m, x = mha(sol, 12, 3), torch.randn(2, 6, 12)
    cm = sol.causal_mask(6)
    with torch.no_grad():
        close_t(m(x, cm), reference(m, 12, 3)(x, x, x, attn_mask=~cm, need_weights=False)[0])


def test_p2_batch_mask(sol):
    m, x = mha(sol), torch.randn(2, 4, 8)
    bm = torch.stack([sol.causal_mask(4), torch.ones(4, 4, dtype=torch.bool)])
    with torch.no_grad():
        out = m(x, bm)
        close_t(out[0], m(x[:1], sol.causal_mask(4))[0])
        close_t(out[1], m(x[1:])[0])


def test_p2_single_head(sol):
    m, x = mha(sol, 4, 1), torch.randn(1, 3, 4)
    with torch.no_grad():
        o, _ = manual(m.q_proj(x), m.k_proj(x), m.v_proj(x))
        close_t(m(x), m.out_proj(o))
