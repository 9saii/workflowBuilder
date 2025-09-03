import time
import random
from openai import RateLimitError

def retry_openai_call(func, max_retries=3, base_delay=1, max_delay=60):
    """
    Retry an OpenAI API call with exponential backoff on rate limit errors.

    Args:
        func: The function to retry (should be a lambda or partial function)
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for exponential backoff
        max_delay: Maximum delay in seconds

    Returns:
        The result of the successful function call

    Raises:
        The last exception if all retries fail
    """
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return func()
        except RateLimitError as e:
            last_exception = e
            if attempt == max_retries:
                break

            # Calculate delay with exponential backoff and jitter
            delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
            print(f"Rate limit exceeded. Retrying in {delay:.2f} seconds... (attempt {attempt + 1}/{max_retries + 1})")
            time.sleep(delay)
        except Exception as e:
            # For non-rate-limit errors, don't retry
            raise e

    # If we get here, all retries failed with rate limit errors
    raise last_exception
