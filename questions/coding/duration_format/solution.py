import re

_PATTERN = re.compile(r"\s*(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:(\d+)s)?\s*", re.I)


def format_duration(seconds):
    """Return a rider friendly string like '1h 05m'."""
    if seconds < 0:
        raise ValueError("negative duration")
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m:02d}m" if m else f"{h}h"
    if m:
        return f"{m}m {s:02d}s" if s else f"{m}m"
    return f"{s}s"


def parse_duration(text):
    """Parse '1h 5m 3s' style text into seconds."""
    m = _PATTERN.fullmatch(text)
    if not m or not any(m.groups()):
        raise ValueError(f"cannot parse {text!r}")
    h, mi, s = (int(g) if g else 0 for g in m.groups())
    return h * 3600 + mi * 60 + s
