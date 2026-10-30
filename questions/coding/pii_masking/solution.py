import re

_EMAIL = re.compile(r"\b([A-Za-z0-9._+-])[A-Za-z0-9._+-]*@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})\b")
_PHONE = re.compile(r"(?<![\d-])(?:\+1 |1-)?(?:\(\d{3}\) |\d{3}[-.]?)\d{3}[-.]?(\d{4})(?![\d-])")


def mask_emails(text):
    """Mask the local part of every email."""
    return _EMAIL.sub(lambda m: f"{m.group(1)}***@{m.group(2)}", text)


def mask_phones(text):
    """Mask every phone number, keeping the last 4 digits."""
    return _PHONE.sub(lambda m: f"***-***-{m.group(1)}", text)


def mask_all(text):
    """Mask emails and phones."""
    return mask_phones(mask_emails(text))
