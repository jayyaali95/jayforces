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

**Example**
```python
>>> calls = []
>>> waits = []
>>> @retry(times=3, delay=1.0, backoff=2.0, sleep=waits.append)
... def flaky():
...     calls.append(1)
...     if len(calls) < 3:
...         raise ConnectionError("down")
...     return "ok"
>>> flaky()
'ok'
>>> waits
[1.0, 2.0]
```

## Part 2: Selective retries and introspection

Add keyword `on=(Exception,)`: only exception types in `on` (and their subclasses) are retried; anything else is raised immediately.
Add keyword `max_delay=None` to cap each wait. The wrapper also exposes `wrapper.attempts`, the number of attempts
made by the most recent call.

**Example**
```python
>>> waits = []
>>> @retry(times=5, delay=1.0, backoff=2.0, sleep=waits.append, on=(ConnectionError,), max_delay=3.0)
... def always_down():
...     raise ConnectionError("x")
>>> always_down()          # raises ConnectionError after 5 attempts
>>> always_down.attempts
5
>>> waits                  # 1, 2, then capped at 3
[1.0, 2.0, 3.0, 3.0]
>>> @retry(times=3, on=(ConnectionError,), sleep=lambda s: None)
... def bad():
...     raise KeyError("k")
>>> bad()                  # KeyError is not in `on`: raised immediately
>>> bad.attempts
1
```
