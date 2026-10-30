import functools
import time


def retry(times=3, delay=0.0, backoff=2.0, sleep=time.sleep, on=(Exception,), max_delay=None):
    """Decorator factory that retries the wrapped call."""
    if times < 1:
        raise ValueError("times must be >= 1")

    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                wrapper.attempts = attempt
                try:
                    return fn(*args, **kwargs)
                except on:
                    if attempt == times:
                        raise
                    sleep(wait if max_delay is None else min(wait, max_delay))
                    wait *= backoff

        wrapper.attempts = 0
        return wrapper

    return deco
