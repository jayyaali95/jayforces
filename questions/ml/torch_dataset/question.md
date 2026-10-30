---
title: Datasets, loaders and padding
difficulty: medium
category: ml
tags: pytorch, Dataset, DataLoader, collate
timeout: 20
---
Feed trip data to a model the PyTorch way.

## Part 1: Tabular dataset

Implement `RideDataset(records)` subclassing `torch.utils.data.Dataset`. Each record is `{"features": [floats], "label": int}`.
All feature lists must have the same length, otherwise raise `ValueError` in the constructor. An empty `records` list is allowed and gives a dataset of length 0.
`dataset[i]` returns `(features, label)` where features is a `float32` tensor of shape `(d,)` and label an `int64` scalar tensor.

Implement `make_loader(dataset, batch_size, shuffle=False, seed=0)` returning a `DataLoader`; when shuffling, pass
`generator=torch.Generator().manual_seed(seed)` so the order is reproducible.

**Example**
```python
>>> ds = RideDataset([{"features": [1.0, 2.0], "label": 0},
...                   {"features": [3.0, 4.0], "label": 1},
...                   {"features": [5.0, 6.0], "label": 1}])
>>> len(ds)
3
>>> ds[1]
(tensor([3., 4.]), tensor(1))
>>> for xb, yb in make_loader(ds, batch_size=2):
...     print(xb.tolist(), yb.tolist())
[[1.0, 2.0], [3.0, 4.0]] [0, 1]
[[5.0, 6.0]] [1]
```

## Part 2: Variable length sequences

GPS traces have different lengths. Implement `SequenceDataset(sequences, labels)` where `sequences[i]` is a list of points
(each a list of `d` floats); items are `(float32 tensor (L_i, d), int64 scalar label)`.

Implement `pad_collate(batch)` returning `(padded, lengths, labels)`: `padded` is `float32 (B, L_max, d)` with zeros after each
sequence, `lengths` an `int64 (B,)` tensor, `labels` `int64 (B,)`, all in batch order. Then `make_seq_loader(dataset, batch_size)`
(no shuffle) uses it.

**Example**
```python
>>> sd = SequenceDataset([[[1., 2.], [3., 4.], [5., 6.]], [[7., 8.]]], [0, 1])
>>> padded, lengths, labels = next(iter(make_seq_loader(sd, batch_size=2)))
>>> padded.shape
torch.Size([2, 3, 2])
>>> padded.tolist()
[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], [[7.0, 8.0], [0.0, 0.0], [0.0, 0.0]]]
>>> lengths, labels
(tensor([3, 1]), tensor([0, 1]))
```
