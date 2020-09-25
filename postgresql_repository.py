import psycopg2

project_board_statement = "SELECT board_id, project_id from board_project_relation"
board_card_statement = "SELECT card_id, board_id from card_board_relation"
comment_card_statement = "SELECT id, card_id from commit"


def connect_postgresql(database, user, password, host, port):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    return cur


def search_table_and_create_subtype_dict(cur, select_statement):
    cur.execute(select_statement)
    subtype_dict = dict()

    select_rows = cur.fetchall()

    for row in select_rows:
        if subtype_dict.get(row[1]) is None:
            subtype_dict[row[1]] = [row[0]]
        else:
            subtype_dict[row[1]].append(row[0])

    return subtype_dict


project_cur = connect_postgresql("scrumproject", "postgres", "postgres", "localhost", "54323")
comment_cur = connect_postgresql("message", "postgres", "postgres", "localhost", "54322")

project_board_dict = search_table_and_create_subtype_dict(project_cur, project_board_statement)
board_card_dict = search_table_and_create_subtype_dict(project_cur, board_card_statement)
comment_card_dict = search_table_and_create_subtype_dict(comment_cur, comment_card_statement)

print("over")
