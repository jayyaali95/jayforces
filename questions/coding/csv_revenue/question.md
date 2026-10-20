---
title: Revenue report from CSV
difficulty: medium
category: coding
tags: csv, parsing, data cleaning
---
Finance exports trips as CSV text with a header row:

```
trip_id,city,fare,currency,completed_at
t1,"San Francisco, CA",12.50,USD,2024-05-01
```

Fields can be quoted (and quoted fields can contain commas). Use the standard library.

## Part 1: Parse and aggregate

Implement `revenue_by_city(csv_text)` returning `{city: total_cents}` (int cents, fare rounded half up
to the cent). Skip a row if it is malformed: wrong number of columns, empty city, a fare that is not a
non negative number, or a currency other than `USD`. Header column order may change; find columns by name.
City names are trimmed.

## Part 2: Report with errors

Implement `report(csv_text)` returning `{"totals": {...}, "errors": [(line_number, reason), ...], "top_city": city_or_None}`.
`line_number` is 1 based including the header (first data row is line 2). Reasons are exactly one of
`"columns"`, `"city"`, `"fare"`, `"currency"`, `"duplicate"` (checked in that order). A `trip_id` seen before in a
valid row is a `"duplicate"` and skipped. `top_city` has the highest total, ties broken alphabetically.
Missing required header columns raise `ValueError`.
