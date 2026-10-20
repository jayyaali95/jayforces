import itertools

import numpy as np

from check import close, eq

START = np.array([0.6, 0.4])
TRANS = np.array([[0.7, 0.3], [0.4, 0.6]])
EMIT = np.array([[0.5, 0.4, 0.1], [0.1, 0.3, 0.6]])
OBS = [0, 1, 2]


def joint(path, obs, s=START, t=TRANS, e=EMIT):
    p = s[path[0]] * e[path[0], obs[0]]
    for a, b, o in zip(path, path[1:], obs[1:]):
        p *= t[a, b] * e[b, o]
    return p


def brute(obs, s=START, t=TRANS, e=EMIT):
    paths = list(itertools.product(range(len(s)), repeat=len(obs)))
    return paths, np.array([joint(p, obs, s, t, e) for p in paths])


def test_p1_matches_brute(sol):
    close(sol.forward_log_prob(OBS, START, TRANS, EMIT), float(np.log(brute(OBS)[1].sum())))


def test_p1_single_obs(sol):
    close(sol.forward_log_prob([2], START, TRANS, EMIT), float(np.log(0.6 * 0.1 + 0.4 * 0.6)))


def test_p1_empty(sol):
    close(sol.forward_log_prob([], START, TRANS, EMIT), 0.0)


def test_p1_longer_brute(sol):
    obs = [2, 2, 0, 1, 0, 2]
    close(sol.forward_log_prob(obs, START, TRANS, EMIT), float(np.log(brute(obs)[1].sum())))


def test_p1_no_underflow(sol):
    lp = sol.forward_log_prob([0, 1, 2] * 1000, START, TRANS, EMIT)
    eq(np.isfinite(lp) and lp < -1000, True)


def test_p1_impossible(sol):
    e = np.array([[1.0, 0.0], [1.0, 0.0]])
    eq(sol.forward_log_prob([1], START, TRANS, e), float("-inf"))


def test_p1_zero_transitions_ok(sol):
    t = np.array([[0.0, 1.0], [1.0, 0.0]])
    close(sol.forward_log_prob([0, 2], START, t, EMIT), float(np.log(brute([0, 2], t=t)[1].sum())))


def test_p2_classic_path(sol):
    path, lp = sol.viterbi(OBS, START, TRANS, EMIT)
    eq(path, [0, 0, 1])
    close(lp, float(np.log(0.01512)))


def test_p2_matches_brute(sol):
    obs = [2, 0, 0, 1, 2, 2, 1]
    paths, probs = brute(obs)
    path, lp = sol.viterbi(obs, START, TRANS, EMIT)
    eq(path, list(paths[int(probs.argmax())]))
    close(lp, float(np.log(probs.max())))


def test_p2_returns_ints(sol):
    eq(all(type(s) is int for s in sol.viterbi(OBS, START, TRANS, EMIT)[0]), True)


def test_p2_long_sequence(sol):
    path, lp = sol.viterbi([0] * 500 + [2] * 500, START, TRANS, EMIT)
    eq((len(path), np.isfinite(lp), path[0], path[-1]), (1000, True, 0, 1))


def test_p2_ties_smaller_state(sol):
    s, t, e = np.array([0.5, 0.5]), np.full((2, 2), 0.5), np.full((2, 1), 1.0)
    eq(sol.viterbi([0, 0, 0], s, t, e)[0], [0, 0, 0])


def test_p2_three_states(sol):
    s = np.array([0.2, 0.5, 0.3])
    t = np.array([[0.5, 0.3, 0.2], [0.2, 0.6, 0.2], [0.1, 0.2, 0.7]])
    e = np.array([[0.7, 0.3], [0.4, 0.6], [0.1, 0.9]])
    obs = [1, 1, 0, 1, 0]
    paths, probs = brute(obs, s, t, e)
    eq(sol.viterbi(obs, s, t, e)[0], list(paths[int(probs.argmax())]))


def test_p2_posteriors_sum(sol):
    close(sol.posteriors([0, 1, 2, 2], START, TRANS, EMIT).sum(1), np.ones(4))


def test_p2_posteriors_brute(sol):
    obs = [0, 2, 1]
    paths, probs = brute(obs)
    exp = np.zeros((3, 2))
    for p, pr in zip(paths, probs):
        for t_, st in enumerate(p):
            exp[t_, st] += pr
    close(sol.posteriors(obs, START, TRANS, EMIT), exp / probs.sum())
