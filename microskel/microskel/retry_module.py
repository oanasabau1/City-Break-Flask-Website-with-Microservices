import random
import time
import functools

import requests
from decouple import config


class RetryStrategy:
    def wait(self, attempt: int):
        pass


class ExponentialBackoff(RetryStrategy):
    def __init__(self, base: int = 1):
        self.base = base

    def wait(self, attempt: int):
        wait_time = self.base * (2 ** attempt)
        time.sleep(wait_time)


class RetryWithJitter(RetryStrategy):
    def __init__(self, base: int = 1, jitter: int = 1):
        self.base = base
        self.jitter = jitter

    def wait(self, attempt: int):
        wait_time = self.base * (2 ** attempt) + random.uniform(0, self.jitter)
        time.sleep(wait_time)


def get_retry_strategy():
    strategy_name = config('RETRY_STRATEGY', default='exponential_backoff')
    base = config('RETRY_BASE', cast=int, default=1)

    if strategy_name == 'retry_with_jitter':
        jitter = config('RETRY_JITTER', cast=int, default=1)
        return RetryWithJitter(base=base, jitter=jitter)
    else:
        return ExponentialBackoff(base=base)


def retry(retry_strategy: RetryStrategy, max_attempts: int = 5, retry_on_statuses: list = None):
    if retry_on_statuses is None:
        retry_on_statuses = [500, 502, 503, 504]  # Default to common retryable statuses

    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    response = func(*args, **kwargs)
                    if isinstance(response, requests.Response) and response.status_code in retry_on_statuses:
                        attempt += 1
                        if attempt == max_attempts:
                            raise requests.exceptions.RequestException(
                                f"Max attempts reached. Status code: {response.status_code}")
                        retry_strategy.wait(attempt)
                    else:
                        return response
                except requests.exceptions.RequestException as e:
                    attempt += 1
                    if attempt == max_attempts:
                        raise
                    retry_strategy.wait(attempt)
                except Exception as e:
                    attempt += 1
                    if attempt == max_attempts:
                        raise
                    retry_strategy.wait(attempt)

        return wrapper_retry

    return decorator_retry
