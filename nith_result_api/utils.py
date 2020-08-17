import sqlite3
import urllib.request, os, threading
from functools import wraps
from time import perf_counter

MAX_ROWS_LIMIT = 1000

def query_db(query, args=tuple(), one=False,limit=0):
    conn = sqlite3.connect('file:nithResult.db?mode=ro',uri=True)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rv = cur.fetchmany(limit)
    conn.close()

    return (rv[0] if rv else None) if one else rv

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

def check_and_set_default(data):
    defaults = {
        'name' : '',
        'branch' : None,
        'roll' : '%',
        'subject_code' : '%',
        'min_cgpi' : 0,
        'max_cgpi' : 10,
        'min_sgpi' : 0,
        'max_sgpi' : 10,
        'sort_by_cgpi': False,
        'limit' : 50,
        'next_cursor' : '0',
    }
    validate = {
        'name' : lambda x: x or defaults['name'],
        'branch' : lambda x: x.upper() if x else defaults['branch'],
        'roll' : lambda x: x.upper() if x else defaults['roll'],
        'subject_code': lambda x: x.upper() if x else defaults['subject_code'],
        'min_cgpi' : lambda x: float(x) if x and 0 <= float(x) <= 10 else defaults['min_cgpi'],
        'max_cgpi' : lambda x: float(x) if x and 0 <= float(x) <= 10 else defaults['max_cgpi'],
        'min_sgpi' : lambda x: float(x) if x and 0 <= float(x) <= 10 else defaults['min_sgpi'],
        'max_sgpi' : lambda x: float(x) if x and 0 <= float(x) <= 10 else defaults['max_sgpi'],
        'sort_by_cgpi' : lambda x: x and x.lower() == 'true',
        'limit' : lambda x: min(int(x),MAX_ROWS_LIMIT) if x and int(x) > 0 else defaults['limit'],
        'next_cursor' : lambda x: x or defaults['next_cursor'],
    }
    assert defaults.keys() == validate.keys(), 'For every arg there must exists a default value and validation function. One of them is missing.'

    for prop in validate:
        data[prop] = validate[prop](data.get(prop))

def make_request(key):
    url = f'https://api.countapi.xyz/hit/nithp/{key}'
    req = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req,timeout=5)

def hit_counter(key):
    def outer(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            try:
                threading.Thread(target=make_request,args=(key,)).start()
            except Exception as e:
                print("API Hit Counter failed", e)
            finally:
                return func(*args,**kwargs)
        return wrapper
    return outer