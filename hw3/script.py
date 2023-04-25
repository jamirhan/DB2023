import json
import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0)

with open('data.json', 'r') as file:
    data = json.load(file)

data = {str(i): item for i, item in enumerate(data)}
data = {str(key): str(val) for key, val in data.items()}


def count_time(name, f):
    start = time.time()
    f()
    print("saving json as {} took {}s".format(name, time.time() - start))


def as_string():
    r.set('json_string', json.dumps(data))


def as_hash():
    local_data = data
    if isinstance(data, list):
        local_data = {i: item for i, item in enumerate(data)}
    r.hset('json_hash', mapping=local_data)


def as_zset():
    r.zadd('json_zset', {json.dumps(data): 0})


def as_list():
    r.lpush('json_list', json.dumps(data))


count_time("string", as_string)
count_time("zset", as_zset)
count_time("list", as_list)
count_time("hset", as_hash)
