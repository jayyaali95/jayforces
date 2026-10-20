import torch
from torch.utils.data import DataLoader, Dataset


class RideDataset(Dataset):
    """Tabular records -> (features, label) tensors."""

    def __init__(self, records):
        dims = {len(r["features"]) for r in records}
        if len(dims) > 1:
            raise ValueError("inconsistent feature lengths")
        self.x = [torch.tensor(r["features"], dtype=torch.float32) for r in records]
        self.y = [torch.tensor(r["label"], dtype=torch.int64) for r in records]

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        return self.x[i], self.y[i]


def make_loader(dataset, batch_size, shuffle=False, seed=0):
    """DataLoader with a seeded generator for reproducible shuffling."""
    gen = torch.Generator().manual_seed(seed) if shuffle else None
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, generator=gen)


class SequenceDataset(Dataset):
    """Variable length point sequences with a label each."""

    def __init__(self, sequences, labels):
        self.seqs = [torch.tensor(s, dtype=torch.float32) for s in sequences]
        self.labels = [torch.tensor(l, dtype=torch.int64) for l in labels]

    def __len__(self):
        return len(self.seqs)

    def __getitem__(self, i):
        return self.seqs[i], self.labels[i]


def pad_collate(batch):
    """Zero pad sequences to the longest one in the batch."""
    seqs, labels = zip(*batch)
    lengths = torch.tensor([len(s) for s in seqs], dtype=torch.int64)
    padded = torch.zeros(len(seqs), int(lengths.max()), seqs[0].shape[1], dtype=torch.float32)
    for i, s in enumerate(seqs):
        padded[i, :len(s)] = s
    return padded, lengths, torch.stack(labels)


def make_seq_loader(dataset, batch_size):
    """Sequential loader that pads each batch."""
    return DataLoader(dataset, batch_size=batch_size, shuffle=False, collate_fn=pad_collate)
