#!/usr/bin/env python3
"""
Cache class with Redis backend
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """Initialize the Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis using a randomly generated key and return the key.

        Args:
            data: The data to be stored, which can be of type str, bytes, int, or float.

        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())  # Generate a random key
        self._redis.set(key, data)  # Store the data in Redis
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, None]:
        """
        Retrieve data from Redis and apply an optional conversion function.

        Args:
            key: The key under which the data is stored.
            fn: Optional. A callable that converts the data back to its original format.

        Returns:
            The retrieved data, optionally converted using fn.
            If the key does not exist, returns None.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis.

        Args:
            key: The key under which the string is stored.

        Returns:
            The string data, decoded from bytes, or None if key does not exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.

        Args:
            key: The key under which the integer is stored.

        Returns:
            The integer data, or None if key does not exist.
        """
        return self.get(key, lambda d: int(d))
