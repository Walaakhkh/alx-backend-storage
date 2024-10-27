#!/usr/bin/env python3
""" Module to fetch web pages with caching """

import redis
import requests
from time import time
from functools import wraps

# Initialize the Redis connection
redis_client = redis.Redis()


def cache_page(method):
    """ Decorator to cache web page content """
    @wraps(method)
    def wrapper(url: str):
        # Create a cache key for the URL
        cache_key = f"cache:{url}"
        # Check if the URL is in cache
        cached_response = redis_client.get(cache_key)

        if cached_response:
            # If cached, return the cached response
            return cached_response.decode('utf-8')

        # Otherwise, call the original method to fetch the page
        response = method(url)

        # Store the response in Redis with an expiration of 10 seconds
        redis_client.setex(cache_key, 10, response)

        # Increment the access count for this URL
        count_key = f"count:{url}"
        redis_client.incr(count_key)

        return response
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """ Get the HTML content of a URL """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))  # Fetch the page
    print(get_page(url))  # Fetch the page again, this time from cache
