#!/usr/bin/env python3
"""
In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of the function
is very simple. It uses the requests module to obtain the HTML
content of a particular URL and returns it
"""
import requests
import redis


r = redis.Redis()


def get_page(url: str) -> str:
    """
    Inside get_page track how many times a particular URL was
    accessed in the key count:{url} and cache the result with
    an expiration time of 10 seconds
    """
    html = r.get(url)
    if html:
        return html.decode('utf-8')
    else:
        response = requests.get(url)
        html = response.text
        r.set(url, html, ex=10)
        return html


if __name__ == "__main__":
    get_page("http://slowwly.robertomurray.co.uk")
