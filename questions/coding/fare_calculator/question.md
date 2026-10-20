---
title: Fare calculator
difficulty: easy
category: coding
tags: money, rounding, validation
---
Price a ride. Money is tricky with floats, so work in **integer cents** internally and only
return cents.

```python
RATES = {"standard": {"base": 250, "per_mile": 150, "per_min": 30, "minimum": 700},
         "xl":       {"base": 400, "per_mile": 250, "per_min": 45, "minimum": 1100}}
```

## Part 1: Base fare

Implement `fare(miles, minutes, ride_type="standard", surge=1.0)` returning cents.

1. `raw = base + per_mile * miles + per_min * minutes`
2. multiply by `surge`
3. round half up to a whole cent (`1234.5` becomes `1235`)
4. never return less than `minimum`

Raise `ValueError` for negative miles or minutes, an unknown ride type, or `surge < 1`.

## Part 2: Promotions

Implement `apply_promo(cents, promo)`. A promo is a dict, one of:

- `{"type": "percent", "value": 20, "cap": 500}`: take `value` percent off (round half up), but at most `cap` cents. `cap` is optional.
- `{"type": "flat", "value": 300}`: take a flat amount off.

The result never goes below 0. `promo=None` returns the fare unchanged. Anything else raises `ValueError`.
