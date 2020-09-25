import psycopg2


def connect_postgresql(database, user="postgres", password="postgres", host="localhost", port="5432"):
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

