---
title: Pricing rule expressions
difficulty: hard
category: coding
tags: parsing, recursion, tokenizer
---
Pricing analysts write rules like `base + 1.5 * (miles - 2)`. Evaluate them safely. **No `eval`**, no `ast` module.

## Part 1: Arithmetic

Implement `evaluate(expr)` supporting non negative numbers (ints and decimals like `2.5` or `.5`), `+ - * /`,
parentheses, unary minus (`-3`, `-(2 + 1)`, `2 * -3`) and arbitrary whitespace. Usual precedence, left associative
(`8 - 3 - 2` is 3, `8 / 4 / 2` is 1). Return a `float`. Raise `ValueError` for malformed input (unbalanced parens,
dangling operators, empty input, unknown characters) and `ZeroDivisionError` for division by zero.

## Part 2: Variables and functions

Extend with `evaluate(expr, variables=None)`. Identifiers (`[A-Za-z_][A-Za-z0-9_]*`) are looked up in
`variables`; unknown names raise `NameError`. Support function calls `min(a, b, ...)` and `max(a, b, ...)`
with one or more arguments; unknown functions raise `NameError`, zero arguments raise `ValueError`.
