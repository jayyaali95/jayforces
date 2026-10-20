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
Each hidden size adds `nn.Linear` then `nn.ReLU`, then `nn.Dropout(dropout)` only when `dropout > 0`. A final `nn.Linear` maps to
`out_dim` (no activation, it outputs logits). `hidden=[]` means a single linear layer.

Implement `count_params(model)` returning the number of **trainable** parameters.

## Part 2: Train and evaluate

Implement `train(model, X, y, epochs=100, lr=0.01, batch_size=32, seed=0)`:
build a `DataLoader(TensorDataset(X, y), batch_size, shuffle=True, generator=torch.Generator().manual_seed(seed))`,
use `torch.optim.Adam` and `nn.CrossEntropyLoss`, put the model in train mode, and return a list with the mean loss of every epoch
(weighted by batch size) as Python floats.

Implement `accuracy(model, X, y)` returning a Python float. It must not track gradients and must leave the model in whatever mode
(train or eval) it was in before the call.
