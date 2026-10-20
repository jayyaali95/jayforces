---
title: Payout ledger reconciliation
difficulty: hard
category: coding
tags: matching, data cleaning, greedy
---
Driver payouts are recorded by us (`internal`) and by the bank (`bank`). Each record is
`{"id": str, "driver": str, "amount": int_cents, "ts": int}`. Reconcile them every night.

## Part 1: Exact match by id

Implement `reconcile(internal, bank)` returning a dict with:

- `"matched"`: sorted list of ids present in both with the same driver and amount
- `"mismatched"`: sorted list of `(id, internal_amount, bank_amount)` present in both but differing in amount or driver
  (when only the driver differs the amounts are still reported)
- `"missing_in_bank"` and `"missing_in_internal"`: sorted id lists

Duplicate ids within one side: keep the last record of that side.

## Part 2: Fuzzy matching

Banks rename ids. Implement `fuzzy_match(internal, bank, window=60, tolerance=0)` that pairs records **ignoring ids**:
same driver, `|amount_diff| <= tolerance`, `|ts_diff| <= window`. Each record is used at most once.
Process internal records sorted by `(ts, id)`; for each, choose among unused candidates the bank record with the
smallest `|ts_diff|`, then smallest `|amount_diff|`, then smallest bank id.
Return `{"pairs": [(internal_id, bank_id), ...], "unmatched_internal": [...], "unmatched_bank": [...]}` where pairs
are in processing order and unmatched lists are sorted.
