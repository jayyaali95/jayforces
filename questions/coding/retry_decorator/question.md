---
title: Retry decorator
difficulty: medium
category: coding
tags: decorators, closures, functools
---
Calls to the maps service fail sometimes. Write a reusable decorator instead of copy-pasting loops.

## Part 1: Basic retry

Implement `retry(times=3, delay=0.0, backoff=2.0, sleep=time.sleep)`, a decorator factory.
The wrapped function is called up to `times` attempts in total. After a failure (any `Exception`) it waits
`delay`, then `delay * backoff`, then `delay * backoff**2`, and so on, using the injected `sleep` function
(tests pass a fake). If the last attempt fails, re-raise that exception. Use `functools.wraps` so the name and
docstring survive. `times < 1` raises `ValueError` when the decorator is created.

## Part 2: Selective retries and introspection

Add keyword `on=(Exception,)`: only exception types in `on` are retried; anything else is raised immediately.
Add keyword `max_delay=None` to cap each wait. The wrapper also exposes `wrapper.attempts`, the number of attempts
made by the most recent call.
