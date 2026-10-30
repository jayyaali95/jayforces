---
title: MLP and training loop in PyTorch
difficulty: medium
category: ml
tags: pytorch, nn.Module, training loop
timeout: 30
---
Write the PyTorch boilerplate you should be able to type in your sleep.

## Part 1: The model

Implement `class MLP(nn.Module)` with `__init__(self, in_dim, hidden, out_dim, dropout=0.0)` where `hidden` is a list of layer sizes.
Each hidden size adds `nn.Linear` then `nn.ReLU`, then `nn.Dropout(dropout)` only when `dropout > 0`. The layers are stored in an `nn.Sequential` kept as `self.net`. A final `nn.Linear` maps to
`out_dim` (no activation, it outputs logits). `hidden=[]` means a single linear layer.

Implement `count_params(model)` returning the number of **trainable** parameters.

**Example**
```python
>>> net = MLP(in_dim=4, hidden=[8, 8], out_dim=3)
>>> [type(m).__name__ for m in net.net]
['Linear', 'ReLU', 'Linear', 'ReLU', 'Linear']
>>> count_params(net)   # (4*8+8) + (8*8+8) + (8*3+3)
139
>>> count_params(MLP(2, [], 2))   # a single Linear(2, 2)
6
```

## Part 2: Train and evaluate

Implement `train(model, X, y, epochs=100, lr=0.01, batch_size=32, seed=0)`:
build a `DataLoader(TensorDataset(X, y), batch_size, shuffle=True, generator=torch.Generator().manual_seed(seed))`,
use `torch.optim.Adam` and `nn.CrossEntropyLoss`, put the model in train mode, and return a list with the mean loss of every epoch
(weighted by batch size) as Python floats.

Implement `accuracy(model, X, y)` returning a Python float. It must not track gradients and must leave the model in whatever mode
(train or eval) it was in before the call.

**Example**
```python
# XOR, 32 samples (the 4 points repeated)
>>> X = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]] * 8)
>>> y = torch.tensor([0, 1, 1, 0] * 8)
>>> torch.manual_seed(0)
>>> net = MLP(2, [8], 2)
>>> losses = train(net, X, y, epochs=100, lr=0.05, batch_size=8)
>>> len(losses), losses[0] > losses[-1]   # one mean loss per epoch, and it went down
(100, True)
>>> accuracy(net, X, y)
1.0
>>> net.training   # mode is left as it was (train() leaves it in train mode)
True
```
