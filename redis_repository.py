import redis
from postgresql_repository import *


def connect_redis(host="127.0.0.1", port=6379, password='', db=0):
    pool = redis.ConnectionPool(host=host, port=port, password=password, db=db)
    client = redis.StrictRedis(connection_pool=pool)

    return client


def push_data_from_postgresql(data_dict, client, table):
    for key in data_dict:
        client.sadd(table + ":" + str(key), *data_dict[key])

