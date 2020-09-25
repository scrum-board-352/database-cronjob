from postgresql_repository import connect_postgresql, search_table_and_create_subtype_dict
from redis_repository import connect_redis, push_data_from_postgresql
import os

project_board_statement = "SELECT board_id, project_id from board_project_relation"
board_card_statement = "SELECT card_id, board_id from card_board_relation"
comment_card_statement = "SELECT id, card_id from commit"

host = os.getenv('host') if None else "127.0.0.1"
postgres_user = os.getenv('postgres_user') if None else "postgres"
postgres_pw = os.getenv('postgres_pw') if None else "postgres"
project_postgres_port = os.getenv('project_postgres_port') if None else "5432"
comment_postgres_port = os.getenv('comment_postgres_port') if None else "5432"
print("host: " + host + "postgres_user" + postgres_user + "postgres_pw" + postgres_pw)

project_cur = connect_postgresql("scrumproject", postgres_user, postgres_pw, host, project_postgres_port)
comment_cur = connect_postgresql("message", postgres_user, postgres_pw, host, comment_postgres_port)

project_board_dict = search_table_and_create_subtype_dict(project_cur, project_board_statement)
board_card_dict = search_table_and_create_subtype_dict(project_cur, board_card_statement)
comment_card_dict = search_table_and_create_subtype_dict(comment_cur, comment_card_statement)

redis_pw = os.getenv('redis_pw')
redis_port = os.getenv('redis_port') if None else "6379"

client = connect_redis(host=host, port=redis_port, password=redis_pw)
push_data_from_postgresql(project_board_dict, client, "project")
push_data_from_postgresql(board_card_dict, client, "board")
push_data_from_postgresql(project_board_dict, client, "project")

print("database_cronjob: over")
