from postgresql_repository import connect_postgresql, search_table_and_create_subtype_dict
from redis_repository import connect_redis, push_data_from_postgresql
import os

user_team_statement = "SELECT team_id, username from user_team_relation"
project_board_statement = "SELECT board_id, project_id from board_project_relation"
board_card_statement = "SELECT card_id, board_id from card_board_relation"
comment_card_statement = "SELECT id, card_id from commit"

host = os.getenv('host') if os.getenv('host') is not None else "127.0.0.1"
postgres_user = os.getenv('postgres_user') if os.getenv('postgres_user') is not None else "postgres"
postgres_pw = os.getenv('postgres_pw') if os.getenv('postgres_pw') is not None else "postgres"
project_postgres_port = os.getenv('postgres_port') if os.getenv('postgres_port') is not None else "5432"
comment_postgres_port = os.getenv('postgres_port') if os.getenv('postgres_port') is not None else "5432"
people_postgres_port = os.getenv('postgres_port') if os.getenv('postgres_port') is not None else "5432"

project_cur = connect_postgresql("scrumproject", postgres_user, postgres_pw, host, project_postgres_port)
comment_cur = connect_postgresql("message", postgres_user, postgres_pw, host, comment_postgres_port)
people_cur = connect_postgresql("people", postgres_user, postgres_pw, host, people_postgres_port)

user_team_dict, team_user_dict = search_table_and_create_subtype_dict(people_cur, user_team_statement)
project_board_dict, board_project_dict = search_table_and_create_subtype_dict(project_cur, project_board_statement)
board_card_dict, card_board_dict = search_table_and_create_subtype_dict(project_cur, board_card_statement)
card_comment_dict, comment_card_dict = search_table_and_create_subtype_dict(comment_cur, comment_card_statement)

redis_pw = os.getenv('redis_pw')
redis_port = os.getenv('redis_port') if os.getenv('redis_port') is not None else "6379"

client_db0 = connect_redis(host=host, port=redis_port, password=redis_pw)
client_db1 = connect_redis(host=host, port=redis_port, password=redis_pw, db=1)
push_data_from_postgresql(user_team_dict, client_db0, "people")
push_data_from_postgresql(project_board_dict, client_db0, "project")
push_data_from_postgresql(board_card_dict, client_db0, "board")
push_data_from_postgresql(card_comment_dict, client_db0, "card")

push_data_from_postgresql(team_user_dict, client_db1, "team")
push_data_from_postgresql(board_project_dict, client_db1, "board")
push_data_from_postgresql(card_board_dict, client_db1, "card")
push_data_from_postgresql(comment_card_dict, client_db1, "comment")

print("database_cronjob: over")
