---
title: Tiny autograd engine
difficulty: hard
category: ml
tags: python, dunder methods, backprop, graphs
---
Build a scalar reverse mode autodiff engine (in the spirit of micrograd). This is as much a Python design question as an ML one.

## Part 1: Values and arithmetic

Implement `class Value` with `data` (float), `grad` (starts `0.0`). Support `a + b`, `a * b`, `-a`, `a - b`, `a / b`, `a ** k`
(k an int or float constant) and the reflected forms with plain numbers (`2 * a`, `1 + a`, `3 - a`, `1 / a`). Add `relu()`, `tanh()`
and `exp()`. Results are new `Value`s that remember their parents.

## Part 2: Backward

Implement `backward()` on the output: set its grad to 1, then visit nodes in **reverse topological order** and accumulate gradients
into parents with `+=` (a value used twice, like `a * a`, must get both contributions). Calling `backward()` must work on graphs with
shared subexpressions and deep chains (10k nodes, so no recursion depth issues). Add `zero_grad()` that resets grads of every node in
the graph to 0.
