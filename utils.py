from time import perf_counter
from functools import wraps

def timer(description):
    def outer(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            start = perf_counter()
            val = func(*args,**kwargs)
            end = perf_counter()
            print(f"⏳ {description}: {end - start}")
            return val
        return wrapper
    return outer

class Timer(object):
    def __init__(self, description):
        self.description = description
    def __enter__(self):
        self.start = perf_counter()
    def __exit__(self, type, value, traceback):
        self.end = perf_counter()
        print(f"⏳ {self.description}: {self.end - self.start}")