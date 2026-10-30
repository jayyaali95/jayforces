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

**Example**
```python
a = Value(2.0)
b = Value(3.0)
c = a * b + a          # Value(data=8.0, grad=0.0)
d = 3 - a              # Value(data=1.0, grad=0.0)
e = 1 / a              # Value(data=0.5, grad=0.0)
f = a ** 3             # Value(data=8.0, grad=0.0)
g = Value(-4.0).relu() # Value(data=0.0, grad=0.0)
```

## Part 2: Backward

Implement `backward()` on the output: set its grad to 1, then visit nodes in **reverse topological order** and accumulate gradients
into parents with `+=` (a value used twice, like `a * a`, must get both contributions). Calling `backward()` must work on graphs with
shared subexpressions and deep chains (10k nodes, so no recursion depth issues). Add `zero_grad()` that resets grads of every node in
the graph to 0.

**Example**
```python
# f = a * a, so df/da = 2a (a is used twice and both contributions accumulate)
a = Value(3.0)
f = a * a
f.backward()
# f -> Value(data=9.0, grad=1.0)
# a -> Value(data=3.0, grad=6.0)

# d = exp(a) + tanh(a) at a = 0: d/da = 1 + 1 = 2
a = Value(0.0)
d = a.exp() + a.tanh()
d.backward()
# d -> Value(data=1.0, grad=1.0)
# a -> Value(data=0.0, grad=2.0)
d.zero_grad()
# a.grad -> 0.0
```
