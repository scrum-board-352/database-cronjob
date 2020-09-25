from postgresql_repository import connect_postgresql, search_table_and_create_subtype_dict
from redis_repository import connect_redis, push_data_from_postgresql

project_board_statement = "SELECT board_id, project_id from board_project_relation"
board_card_statement = "SELECT card_id, board_id from card_board_relation"
comment_card_statement = "SELECT id, card_id from commit"

project_cur = connect_postgresql("scrumproject", "postgres", "postgres", "localhost", "54323")
comment_cur = connect_postgresql("message", "postgres", "postgres", "localhost", "54322")

project_board_dict = search_table_and_create_subtype_dict(project_cur, project_board_statement)
board_card_dict = search_table_and_create_subtype_dict(project_cur, board_card_statement)
comment_card_dict = search_table_and_create_subtype_dict(comment_cur, comment_card_statement)

client = connect_redis()
push_data_from_postgresql(project_board_dict, client, "project")
push_data_from_postgresql(board_card_dict, client, "board")
push_data_from_postgresql(project_board_dict, client, "project")

print("over")
