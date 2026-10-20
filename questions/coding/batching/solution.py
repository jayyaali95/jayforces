from itertools import islice


def batched(iterable, size):
    """Yield lists of up to `size` items."""
    if size < 1:
        raise ValueError("size must be >= 1")
    it = iter(iterable)
    while chunk := list(islice(it, size)):
        yield chunk


def batched_by_weight(iterable, max_weight, weight=len):
    """Yield lists whose total weight stays within max_weight."""
    batch, total = [], 0
    for item in iterable:
        w = weight(item)
        if batch and total + w > max_weight:
            yield batch
            batch, total = [], 0
        batch.append(item)
        total += w
        if total > max_weight:
            yield batch
            batch, total = [], 0
    if batch:
        yield batch
