---
title: Bike dock stations
difficulty: medium
category: coding
tags: classes, validation, state
---
Lyft bikes live in dock stations. Each station has a fixed number of docks.

## Part 1: Rent and return

Implement `BikeNetwork(stations)` where `stations` is `{station_id: (capacity, bikes)}`. Raise `ValueError`
if any station has `bikes > capacity` or negative numbers.

- `rent(station, rider)`: if the station has a bike and the rider has no active rental, take one and return `True`; otherwise `False`.
- `give_back(station, rider)`: if the rider has an active rental and the station has a free dock, return it and give `True`; otherwise `False`.
- `bikes(station)` returns current bikes. Unknown stations raise `KeyError` for every method.

## Part 2: Rebalancing

Vans move bikes at night. Implement `rebalance_plan(low=0.2, high=0.8)` returning a list of moves
`(from_station, to_station, count)`. Fill rate is `bikes / capacity`. Stations above `high` are donors, below `low`
are receivers. A receiver wants bikes until it reaches `ceil(low * capacity)`; a donor gives bikes down to
`floor(high * capacity)`. Process receivers by lowest fill rate first (ties by id), take from donors with the highest
fill rate first (ties by id), moving as many as possible each step. Do not apply the moves.
