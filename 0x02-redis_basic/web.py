#!/usr/bin/env python3
"""
In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of the function
is very simple. It uses the requests module to obtain the HTML
content of a particular URL and returns it
"""
import requests
import redis
redis = redis.Redis()


def get_page(url: str) -> str:
    """
    Start in a new file named web.py and do not reuse
    the code written in exercise.py
    """
    count_key = "count:{url}"
    redis.incr(count_key)

    result = redis.get(url)
    if result is not None:
        return result

    result = requests.get(url).text
    redis.set(url, result, ex=10)
    return result


if __name__ == "__main__":
    get_page("http://slowwly.robertomurray.co.uk")
