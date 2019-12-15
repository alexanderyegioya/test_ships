import sqlite3
import os
from random import randint
from collections import namedtuple

from sql_templates import (
    weapons_sql_template,
    hulls_sql_template,
    engines_sql_template,
    ships_sql_template
)


def restore_db_from_dump(dump_filename, cursor):
    with open(dump_filename) as f:
        sql = f.read()
        cursor.executescript(sql)


DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'db/ships.db')

TableDetails = namedtuple(
    'TableDetails',
    (
        'table_name',
        'fields',
        'number_of_rows_to_insert',
        'insert_data_sql_template',
        'key_field'
    )
)

weapons_table = TableDetails(
    table_name='weapons',
    fields=(
        'weapon', 'reload_speed', 'rotational_speed',
        'diameter', 'power_volley', 'count'
    ),
    number_of_rows_to_insert=20,
    insert_data_sql_template=weapons_sql_template,
    key_field='weapon',
)

hulls_table = TableDetails(
    table_name='hulls',
    fields=(
        'hull', 'armor', 'type', 'capacity'
    ),
    number_of_rows_to_insert=5,
    insert_data_sql_template=hulls_sql_template,
    key_field='hull'
)

engines_table = TableDetails(
    table_name='engines',
    fields=(
        'engine', 'power', 'type'
    ),
    number_of_rows_to_insert=6,
    insert_data_sql_template=engines_sql_template,
    key_field='engine'
)

ships_table = TableDetails(
    table_name='ships',
    fields=(
        'ship', 'weapon', 'hull', 'engine'
    ),
    number_of_rows_to_insert=201,
    insert_data_sql_template=ships_sql_template,
    key_field='ship'
)

TABLES = (
    # hulls_table,
    # weapons_table,
    # engines_table,
    ships_table,
)


def db_connect(db_path=DEFAULT_PATH):
    conn = sqlite3.connect(db_path)
    return conn


def update_key_value(row, table_details):
    row[1].update(
        {
            table_details.fields[0]: '{item_name}-{order_number}'.format(
                item_name=table_details.fields[0].capitalize(),
                order_number=row[0]
            )
        }
    )


def generate_params_for_query(table_details):
    table_data = [
        {
            field: randint(
                i, 100
            ) for field in table_details.fields if field not in (
            field[0], randint(1, 3)
        )
        } for i in range(1, table_details.number_of_rows_to_insert)
    ]

    for t in enumerate(table_data):
        update_key_value(t, table_details)

    return tuple(table_data)


def generate_params_for_ships_query(table_details):
    table_data = []

    for i in range(1, table_details.number_of_rows_to_insert):
        f = {}
        for field in table_details.fields:
            if 'weapon' in field:
                f['weapon'] = randint(1, 20)
            if 'hull' in field:
                f['hull'] = randint(1, 5)
            if 'engine' in field:
                f['engine'] = randint(1, 6)

        table_data.append(f)

    for t in enumerate(table_data):
        update_key_value(t, table_details)

    return tuple(table_data)


def fill_db_with_data(table_details, conn, cursor):
    cursor.execute('DELETE FROM {table_name}'.format(
        table_name=table_details.table_name)
    )
    conn.commit()

    if table_details.table_name == 'ships':
        params = generate_params_for_ships_query(table_details)
        cursor.executemany(table_details.insert_data_sql_template, params)
        conn.commit()
    else:
        params = generate_params_for_query(table_details)
        cursor.executemany(table_details.insert_data_sql_template, params)
        conn.commit()


conn = db_connect()
cursor = conn.cursor()
# restore_db_from_dump('db/init_db.sql', cursor)

if __name__ == '__main__':
    for t in TABLES:
        fill_db_with_data(t, conn, cursor)
