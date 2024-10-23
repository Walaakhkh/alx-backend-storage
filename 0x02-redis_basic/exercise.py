#!/usr/bin/env python3
"""
Cache class with Redis backend
"""
import redis
import uuid
from typing import Union


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
