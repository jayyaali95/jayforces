import torch
from torch.utils.data import Dataset

from check import eq, raises

RECS = [{"features": [float(i), float(i) * 2], "label": i % 3} for i in range(10)]


def test_p1_is_dataset(sol):
    eq(isinstance(sol.RideDataset(RECS), Dataset), True)


def test_p1_len(sol):
    eq(len(sol.RideDataset(RECS)), 10)


def test_p1_item_types(sol):
    x, y = sol.RideDataset(RECS)[4]
    eq((x.dtype, tuple(x.shape), y.dtype, tuple(y.shape)), (torch.float32, (2,), torch.int64, ()))


def test_p1_item_values(sol):
    x, y = sol.RideDataset(RECS)[4]
    eq((x.tolist(), int(y)), ([4.0, 8.0], 1))


def test_p1_mismatch(sol):
    raises(ValueError, sol.RideDataset, [{"features": [1.0], "label": 0}, {"features": [1.0, 2.0], "label": 0}])


def test_p1_empty(sol):
    eq(len(sol.RideDataset([])), 0)


def test_p1_loader_batches(sol):
    shapes = [tuple(x.shape) for x, _ in sol.make_loader(sol.RideDataset(RECS), 4)]
    eq(shapes, [(4, 2), (4, 2), (2, 2)])


def test_p1_loader_order(sol):
    xs = torch.cat([x for x, _ in sol.make_loader(sol.RideDataset(RECS), 3)])
    eq(xs[:, 0].tolist(), [float(i) for i in range(10)])


def order(sol, seed):
    return torch.cat([x for x, _ in sol.make_loader(sol.RideDataset(RECS), 3, shuffle=True, seed=seed)])[:, 0].tolist()


def test_p1_shuffle_reproducible(sol):
    eq(order(sol, 7), order(sol, 7))


def test_p1_shuffle_changes_order(sol):
    eq(order(sol, 7) != [float(i) for i in range(10)] or order(sol, 8) != [float(i) for i in range(10)], True)


def test_p1_shuffle_covers_all(sol):
    eq(sorted(order(sol, 3)), [float(i) for i in range(10)])


SEQS = [[[1.0, 1.0]], [[2.0, 2.0], [3.0, 3.0], [4.0, 4.0]], [[5.0, 5.0], [6.0, 6.0]]]


def test_p2_seq_item(sol):
    x, y = sol.SequenceDataset(SEQS, [0, 1, 2])[1]
    eq((tuple(x.shape), x.dtype, int(y)), ((3, 2), torch.float32, 1))


def test_p2_collate_shapes(sol):
    ds = sol.SequenceDataset(SEQS, [0, 1, 2])
    p, l, y = sol.pad_collate([ds[0], ds[1], ds[2]])
    eq((tuple(p.shape), l.tolist(), y.tolist()), ((3, 3, 2), [1, 3, 2], [0, 1, 2]))


def test_p2_collate_zeros(sol):
    ds = sol.SequenceDataset(SEQS, [0, 1, 2])
    p, _, _ = sol.pad_collate([ds[0], ds[2]])
    eq(p.tolist(), [[[1.0, 1.0], [0.0, 0.0]], [[5.0, 5.0], [6.0, 6.0]]])


def test_p2_collate_dtypes(sol):
    ds = sol.SequenceDataset(SEQS, [0, 1, 2])
    p, l, y = sol.pad_collate([ds[0]])
    eq((p.dtype, l.dtype, y.dtype), (torch.float32, torch.int64, torch.int64))


def test_p2_seq_loader(sol):
    ds = sol.SequenceDataset(SEQS, [0, 1, 2])
    batches = [(tuple(p.shape), l.tolist()) for p, l, _ in sol.make_seq_loader(ds, 2)]
    eq(batches, [((2, 3, 2), [1, 3]), ((1, 2, 2), [2])])
