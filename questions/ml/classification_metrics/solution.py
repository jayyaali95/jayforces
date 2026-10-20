import numpy as np


def _check(y_true, y_pred):
    t, p = np.asarray(y_true), np.asarray(y_pred)
    if t.shape != p.shape or t.size == 0:
        raise ValueError("inputs must be non empty and the same length")
    return t, p


def _div(a, b):
    return float(a / b) if b else 0.0


def binary_metrics(y_true, y_pred):
    """Return accuracy, precision, recall and f1 for 0/1 labels."""
    t, p = _check(y_true, y_pred)
    tp = np.sum((t == 1) & (p == 1))
    fp = np.sum((t == 0) & (p == 1))
    fn = np.sum((t == 1) & (p == 0))
    prec, rec = _div(tp, tp + fp), _div(tp, tp + fn)
    return {"accuracy": float(np.mean(t == p)), "precision": prec, "recall": rec, "f1": _div(2 * prec * rec, prec + rec)}


def confusion_matrix(y_true, y_pred, labels=None):
    """Return counts M[i, j] of true labels[i] predicted as labels[j]."""
    t, p = _check(y_true, y_pred)
    labels = sorted(set(t.tolist()) | set(p.tolist())) if labels is None else list(labels)
    idx = {lab: i for i, lab in enumerate(labels)}
    m = np.zeros((len(labels), len(labels)), dtype=int)
    for a, b in zip(t.tolist(), p.tolist()):
        if a in idx and b in idx:
            m[idx[a], idx[b]] += 1
    return m


def macro_f1(y_true, y_pred):
    """Unweighted mean F1 over all labels seen."""
    m = confusion_matrix(y_true, y_pred)
    tp = np.diag(m)
    prec = np.divide(tp, m.sum(axis=0), out=np.zeros(len(tp)), where=m.sum(axis=0) > 0)
    rec = np.divide(tp, m.sum(axis=1), out=np.zeros(len(tp)), where=m.sum(axis=1) > 0)
    f1 = np.divide(2 * prec * rec, prec + rec, out=np.zeros(len(tp)), where=(prec + rec) > 0)
    return float(f1.mean())
