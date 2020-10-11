import psycopg2


def connect_postgresql(database, user="postgres", password="postgres", host="localhost", port="5432"):
    conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    return cur


def search_table_and_create_subtype_dict(cur, select_statement):
    cur.execute(select_statement)
    subtype_dict1 = dict()
    subtype_dict2 = dict()

    select_rows = cur.fetchall()

    for row in select_rows:
        if subtype_dict1.get(row[1]) is None:
            subtype_dict1[row[1]] = [row[0]]
        else:
            subtype_dict1[row[1]].append(row[0])

    for row in select_rows:
        if subtype_dict2.get(row[0]) is None:
            subtype_dict2[row[0]] = [row[1]]
        else:
            subtype_dict2[row[0]].append(row[1])

    return subtype_dict1, subtype_dict2

