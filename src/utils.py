"""Utility helpers: logging, simple retry decorator, and safe filenames."""

import logging
import re
import time
from functools import wraps
from pathlib import Path
from typing import Callable, Type, Union

logger = logging.getLogger("researchmate.utils")


def safe_filename(s: str) -> str:
    """Return a filesystem-safe filename derived from `s`.

    Replaces any character that's not alphanumeric, dash, underscore, dot or space
    with an underscore, then replaces spaces with underscores and strips the result.
    """
    s = re.sub(r"[^0-9a-zA-Z\-_\. ]+", "_", s)
    return s.strip().replace(" ", "_")


def ensure_dir(path: Union[str, Path]) -> Path:
    """Create `path` (and parents) if it does not exist and return a Path object."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def retry(on_exception: Union[Type[BaseException], tuple], tries: int = 3, delay: float = 1.0) -> Callable:
    """A decorator factory that retries the wrapped function on `on_exception`.

    Args:
        on_exception: Exception class or tuple of exception classes to catch and retry on.
        tries: Number of attempts (including the first).
        delay: Seconds to wait between attempts.
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, tries + 1):
                try:
                    return fn(*args, **kwargs)
                except on_exception as e:
                    last_exc = e
                    logger.debug("Attempt %d/%d failed: %s", attempt, tries, e)
                    if attempt == tries:
                        logger.error("All %d attempts failed.", tries)
                        raise
                    time.sleep(delay)
            # If we exit the loop without returning, re-raise the last exception
            if last_exc:
                raise last_exc
        return wrapper

    return decorator
