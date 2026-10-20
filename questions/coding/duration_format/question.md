---
title: Trip duration formatting
difficulty: easy
category: coding
tags: strings, parsing
---
Trip durations are shown to riders like `1h 05m` and typed back by support agents like `1h 5m 3s`.

## Part 1: Format

Implement `format_duration(seconds)` for a non negative int:

- under a minute: `"45s"`
- under an hour: minutes and seconds, `"3m 07s"` (seconds always two digits; drop seconds when 0, so `"3m"`)
- an hour or more: hours and minutes, `"1h 05m"`, seconds are truncated; drop minutes when 0, so `"2h"`
- `0` gives `"0s"`

Raise `ValueError` for negative input.

## Part 2: Parse

Implement `parse_duration(text)` returning seconds. Accept any combination of `<n>h`, `<n>m`, `<n>s`
in that order, each at most once, separated by optional whitespace, case insensitive, with leading
zeros allowed (`"1h 05m"` works). Empty strings, wrong order, repeats and junk raise `ValueError`.
