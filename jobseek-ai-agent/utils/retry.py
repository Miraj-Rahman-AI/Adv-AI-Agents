import time
from functools import wraps


def retry(max_attempts=3, delay=2, backoff=2):
    """
    Retry decorator for unstable operations like network calls.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            wait = delay

            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    attempts += 1

                    if attempts >= max_attempts:
                        raise

                    time.sleep(wait)
                    wait *= backoff

        return wrapper

    return decorator
