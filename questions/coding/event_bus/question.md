---
title: Event bus
difficulty: medium
category: coding
tags: design, callbacks, patterns
---
Build the tiny in-process pub/sub that ties ride services together.

## Part 1: Subscribe and publish

Implement `EventBus` with:

- `subscribe(pattern, handler)` returns a subscription token (any hashable). Patterns are dot separated topics
  where a `*` segment matches exactly one segment: `rides.*` matches `rides.created` but not `rides` or `rides.a.b`.
- `publish(topic, payload)` calls every matching handler as `handler(topic, payload)` in subscription order and
  returns how many handlers were called.

## Part 2: Robustness

- `unsubscribe(token)` removes a subscription and returns `True`, or `False` for unknown tokens.
- A `#` segment at the end of a pattern matches **one or more** trailing segments: `rides.#` matches `rides.a` and `rides.a.b`.
- A handler that raises must not stop the others. Publish still returns the number of handlers called (including the
  failing ones) and the exceptions are collected: `errors()` returns `[(topic, exception), ...]` in order.
- Subscribing or unsubscribing from inside a handler must not affect the publish in progress.
