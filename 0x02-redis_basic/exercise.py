#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance
of the Redis client as a private variable named _redis
(using redis.Redis()) and flush the instance using flushdb
"""
import redis
import uuid
from typing import Union, Callable, TypeVar
import functools


T = TypeVar("T", str, bytes, int, float)


def call_history(method: Callable) -> Callable:
    """
    call_history has a single parameter named method
    that is a Callable and returns a Callable
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Execute the wrapped function to retrieve the output.
        Store the output using rpush in the "...:outputs" list,
        then return the output
        """
        key_input = method.__qualname__ + ":inputs"
        key_output = method.__qualname__ + ":outputs"
        self._redis.rpush(key_input, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(key_output, str(output))

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    Above Cache define a count_calls decorator that takes
    a single method Callable argument and returns a Callable
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Remember that the first argument of the wrapped
        function will be self which is the instance itself,
        which lets you access the Redis instance
        """
        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    class Cache
    """
    def __init__(self):
        """
        In the __init__ method, store an instance of the Redis
        client as a private variable named _redis
        (using redis.Redis()) and flush the instance using flushdb
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        method that takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and
        return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn:
            Callable[[bytes], T] = None) -> Union[str, bytes, int, float]:
        """
        method that take a key string argument and an optional
        Callable argument named fn. This callable will be used
        to convert the data back to the desired format
        """
        data = self._redis.get(key)

        if data is None:
            return None

        if fn is not None:
            return fn(data)

        return data

    def get_str(self, key: str) -> str:
        """
         that will automatically parametrize Cache.get
         with the correct conversion function (str)
        """
        return self.get(key, lambda i: i.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
         that will automatically parametrize Cache.get
         with the correct conversion function (int)
        """
        return self.get(key, int)


def replay(method: Callable):
    """
    In this tasks, we will implement a replay function to
    display the history of calls of a particular function
    """
    key_input = method.__qualname__ + ":inputs"
    key_output = method.__qualname__ + ":outputs"

    inputs = method.__self__._redis.lrange(key_input, 0, -1)
    outputs = method.__self__._redis.lrange(key_output, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        i = inp.decode("utf-8")
        o = out.decode("utf-8")
        print("{}(*{}) -> {}".format(method.__qualname__, i, o))
