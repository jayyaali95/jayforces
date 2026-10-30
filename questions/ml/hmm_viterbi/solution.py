import numpy as np


def _logs(start, trans, emit):
    with np.errstate(divide="ignore"):
        return np.log(np.asarray(start, float)), np.log(np.asarray(trans, float)), np.log(np.asarray(emit, float))


def _lse(a, axis):
    m = np.max(a, axis=axis, keepdims=True)
    m = np.where(np.isfinite(m), m, 0.0)
    with np.errstate(divide="ignore"):
        return np.squeeze(m, axis) + np.log(np.exp(a - m).sum(axis))


def _alpha(obs, ls, lt, le):
    a = [ls + le[:, obs[0]]]
    for o in obs[1:]:
        a.append(_lse(a[-1][:, None] + lt, 0) + le[:, o])
    return np.array(a)


def forward_log_prob(obs, start, trans, emit):
    """log P(obs) via the forward algorithm."""
    if len(obs) == 0:
        return 0.0
    return float(_lse(_alpha(obs, *_logs(start, trans, emit))[-1], 0))


def viterbi(obs, start, trans, emit):
    """Most likely hidden path and its log probability."""
    ls, lt, le = _logs(start, trans, emit)
    delta, back = ls + le[:, obs[0]], []
    for o in obs[1:]:
        scores = delta[:, None] + lt
        back.append(scores.argmax(0))
        delta = scores.max(0) + le[:, o]
    path = [int(delta.argmax())]
    for b in reversed(back):
        path.append(int(b[path[-1]]))
    return path[::-1], float(delta.max())


def posteriors(obs, start, trans, emit):
    """P(state_t | obs) for every t."""
    ls, lt, le = _logs(start, trans, emit)
    a = _alpha(obs, ls, lt, le)
    b = [np.zeros(len(ls))]
    for o in reversed(obs[1:]):
        b.append(_lse(lt + (le[:, o] + b[-1])[None, :], 1))
    b = np.array(b[::-1])
    post = a + b
    return np.exp(post - _lse(post, 1)[:, None])
