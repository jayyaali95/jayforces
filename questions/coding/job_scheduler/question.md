---
title: Job dependency scheduler
difficulty: hard
category: coding
tags: graphs, topological sort, scheduling
---
Nightly data jobs depend on each other. `deps` is `{job: [jobs it depends on]}`. A job mentioned only as a
dependency still exists (with no dependencies of its own).

## Part 1: Order

Implement `run_order(deps)` returning a list of all jobs such that every job comes after its dependencies.
When several jobs are ready at the same time, pick the alphabetically smallest first (so the answer is unique).
If there is a cycle raise `ValueError` whose message contains the jobs on one cycle, e.g. `"cycle: a -> b -> a"`.

## Part 2: Parallel stages

Implement `stages(deps)` returning a list of sorted lists: stage 0 holds jobs with no dependencies, and each job
sits in the earliest stage after all its dependencies.

## Part 3: Critical path

Each job has a duration `durations[job]` (missing means 1). With unlimited workers, implement
`finish_time(deps, durations)` returning the total wall time, and `critical_path(deps, durations)` returning the
longest chain of jobs as a list from first to last. To break ties, start from the job that finishes last
(alphabetically smallest if several) and walk backwards, each time picking the alphabetically smallest
dependency that finishes exactly when the current job starts.
