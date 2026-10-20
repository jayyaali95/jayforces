---
title: Hidden Markov model decoding
difficulty: hard
category: ml
tags: dynamic programming, probability, log space
---
A driver's hidden state (`0 = driving`, `1 = waiting`, ...) emits observed GPS speed buckets. Given
`start (S,)`, `trans (S, S)` with `trans[i, j] = P(next=j | cur=i)`, and `emit (S, O)`, work with an observation list `obs` of ints.
Long sequences must not underflow: work in log space (use `np.log` and log-sum-exp; zero probabilities become `-inf`).

## Part 1: Likelihood

Implement `forward_log_prob(obs, start, trans, emit)` returning `log P(obs)` with the forward algorithm.
Empty `obs` gives `0.0`.

## Part 2: Viterbi

Implement `viterbi(obs, start, trans, emit)` returning `(path, log_prob)` for the most likely state sequence.
On ties pick the smaller previous state index during the recursion and the smaller final state.
Also implement `posteriors(obs, start, trans, emit)` returning `(T, S)` state marginals `P(state_t = s | obs)` with forward backward.
