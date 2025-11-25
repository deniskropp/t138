# src/error_handling.py
"""Implements application-wide error handling, including exception wrappers and retry mechanisms."""
import logging
from functools import wraps
import time

logger = logging.getLogger(__name__)

def handle_exception(func):
    """Decorator to log and handle exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            # Depending on policy, re-raise, return default, etc.
            raise
    return wrapper

def retry_policy(retries: int = 3, delay: int = 1):
    """Decorator to retry a function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {i+1}/{retries} failed for {func.__name__}: {e}")
                    time.sleep(delay)
            raise Exception(f"Function {func.__name__} failed after {retries} attempts.")
        return wrapper
    return decorator
