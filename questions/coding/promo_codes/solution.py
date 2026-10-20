import string

ALLOWED = set(string.ascii_uppercase + string.digits)


def is_valid_code(code):
    """Return True when the code passes every format rule."""
    if not isinstance(code, str):
        return False
    c = code.strip().upper()
    return (6 <= len(c) <= 12 and set(c) <= ALLOWED and any(ch.isalpha() for ch in c)
            and any(ch.isdigit() for ch in c) and not c[0].isdigit())


def normalize(code):
    """Return the canonical form of a code or raise ValueError."""
    if not is_valid_code(code):
        raise ValueError(f"invalid promo code {code!r}")
    return code.strip().upper()


class PromoBook:
    """Tracks codes, their limits and who used them."""

    def __init__(self):
        self.codes = {}

    def create(self, code, max_uses, expires_at):
        c = normalize(code)
        if c in self.codes:
            raise ValueError("duplicate code")
        self.codes[c] = {"max": max_uses, "exp": expires_at, "users": set()}

    def redeem(self, code, user, now):
        if not is_valid_code(code):
            return False
        p = self.codes.get(normalize(code))
        if not p or now >= p["exp"] or len(p["users"]) >= p["max"] or user in p["users"]:
            return False
        p["users"].add(user)
        return True
