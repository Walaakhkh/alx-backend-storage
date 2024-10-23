#!/usr/bin/env python3
""" Module for Redis Cache """

import redis
from typing import Callable, Union
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Count how many times methods are called """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function to count calls """
        key = f"{method.__qualname__}"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Store the history of inputs and outputs of the method """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function to store call history """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))  # store inputs
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))  # store outputs

        return result
    return wrapper


class Cache:
    def __init__(self):
        """ Initialize the Cache class """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store the data in Redis and return a random key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        """ Get data from Redis and optionally transform it """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Get string from Redis """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """ Get integer from Redis """
        return self.get(key, lambda d: int(d))


def replay(method: Callable):
    """ Display the history of calls to a particular function """
    redis_instance = method.__self__._redis
    method_name = method.__qualname__

    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"

    # Retrieve input and output data from Redis
    inputs = redis_instance.lrange(inputs_key, 0, -1)
    outputs = redis_instance.lrange(outputs_key, 0, -1)

    # Print number of times the method was called
    print(f"{method_name} was called {len(inputs)} times:")

    # Use zip to pair inputs and outputs and display each call
    for input_, output in zip(inputs, outputs):
        input_str = input_.decode('utf-8')
        output_str = output.decode('utf-8')
        print(f"{method_name}(*{input_str}) -> {output_str}")


# Example usage:
if __name__ == "__main__":
    cache = Cache()

    cache.store("foo")
    cache.store("bar")
    cache.store(42)

    replay(cache.store)
