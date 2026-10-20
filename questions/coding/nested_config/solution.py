import copy


def flatten(config, sep="."):
    """Return {'a.b.c': leaf} for a nested dict."""
    out = {}

    def walk(node, prefix):
        for k, v in node.items():
            if not isinstance(k, str):
                raise TypeError(f"key {k!r} is not a string")
            if sep in k:
                raise ValueError(f"key {k!r} contains {sep!r}")
            key = f"{prefix}{sep}{k}" if prefix else k
            if isinstance(v, dict) and v:
                walk(v, key)
            else:
                out[key] = v

    walk(config, "")
    return out


def unflatten(flat, sep="."):
    """Inverse of flatten. Raises ValueError on conflicts."""
    out = {}
    for key, value in flat.items():
        parts = key.split(sep)
        for i in range(1, len(parts)):
            if sep.join(parts[:i]) in flat:
                raise ValueError(f"{key!r} conflicts with {sep.join(parts[:i])!r}")
        node = out
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = copy.deepcopy(value)
    return out


def deep_merge(base, override):
    """Return a new dict with override applied on top of base."""
    out = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out
