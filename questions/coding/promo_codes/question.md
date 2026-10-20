---
title: Promo codes
difficulty: easy
category: coding
tags: validation, classes
---
Marketing hands out promo codes. Validate them before anything else touches the database.

## Part 1: Format

Implement `is_valid_code(code)`. A valid code:

- is a `str` of 6 to 12 characters after stripping surrounding whitespace
- uses only `A-Z` and `0-9` once uppercased (so `ride20` is fine)
- contains at least one letter and at least one digit
- does not start with a digit

Also implement `normalize(code)` returning the stripped, uppercased code, or raising `ValueError` if invalid.

## Part 2: Redemption

Implement class `PromoBook`:

- `create(code, max_uses, expires_at)` registers a code (normalized). Creating an existing code raises `ValueError`.
- `redeem(code, user, now)` returns `True` and records the use when the code exists, `now < expires_at`,
  total uses are below `max_uses`, and this user has not redeemed it yet. Otherwise returns `False`.
  Codes are matched after normalizing; an invalid code just returns `False`.
