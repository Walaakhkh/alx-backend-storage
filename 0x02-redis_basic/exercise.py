#!/usr/bin/env python3
"""
Cache class with Redis backend, including call history tracking.
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method.

    Args:
        method: The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that records inputs and outputs to Redis."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments as a string in the inputs list
        self._redis.rpush(input_key, str(args))

        # Execute the original method
        result = method(self, *args, **kwargs)

        # Store the output in the outputs list
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.

    Args:
        method: The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments the call count in Redis."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    def __init__(self):
        """Initialize the Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis using a randomly generated key and return the key.

        Args:
            data: The data to be stored, which can be of type str, bytes,
                  int, or float.

        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, None]:
        """
        Retrieve data from Redis and apply an optional conversion function.

        Args:
            key: The key under which the data is stored.
            fn: Optional. A callable that converts the data back to its
                original format.

        Returns:
            The retrieved data, optionally converted using fn.
            If the key does not exist, returns None.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve a string from Redis."""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve an integer from Redis."""
        return self.get(key, lambda d: int(d))


if __name__ == "__main__":
    cache = Cache()

    s1 = cache.store("first")
    print(s1)

    s2 = cache.store("second")
    print(s2)

    s3 = cache.store("third")
    print(s3)

    inputs = cache._redis.lrange(f"{cache.store.__qualname__}:inputs", 0, -1)
    outputs = cache._redis.lrange(f"{cache.store.__qualname__}:outputs", 0, -1)

    print("inputs:", inputs)
    print("outputs:", outputs)
