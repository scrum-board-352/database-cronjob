import redis
from postgresql_repository import *


def connect_redis(host, port, password='', db=0):
    pool = redis.ConnectionPool(host=host, port=port, password=password, db=db)
    client = redis.StrictRedis(connection_pool=pool)

    return client


def push_data_from_postgresql(data_dict, client, table):
    for key in data_dict:
        client.lpush(table + ":" + str(key), *data_dict[key])


project_cur = connect_postgresql("scrumproject", "postgres", "postgres", "localhost", "54323")
comment_cur = connect_postgresql("message", "postgres", "postgres", "localhost", "54322")

project_board_dict = search_table_and_create_subtype_dict(project_cur, project_board_statement)
board_card_dict = search_table_and_create_subtype_dict(project_cur, board_card_statement)
comment_card_dict = search_table_and_create_subtype_dict(comment_cur, comment_card_statement)

client = connect_redis("127.0.0.1", 6379)
push_data_from_postgresql(project_board_dict, client, "project")

print("over")
