import os
import sqlite3

from fill_db import (
    TABLES,
    restore_db_from_dump,
    fill_db_with_data,
    make_dump,
    dict_factory,
    is_initial_insert,
    update_db_data)
from sql_templates import ship_info_sql_template

CURRENT_DB = os.path.join(os.path.dirname(__file__), 'db/ships.db')
DUMP_DB = os.path.join(os.path.dirname(__file__), 'db/dump.db')

conn = sqlite3.connect(CURRENT_DB)

cursor = conn.cursor()

if is_initial_insert(cursor):
    restore_db_from_dump('db/init_db.sql', cursor)
    # fill current_db by data
    for t in TABLES:
        fill_db_with_data(t, conn, cursor, is_initial_insert(cursor))

# make dump of current_db
make_dump(conn)
conn.row_factory = dict_factory
cursor = conn.cursor()

conn2 = sqlite3.connect(DUMP_DB)
conn2.row_factory = dict_factory
cursor2 = conn2.cursor()

# restore from dump
try:
    restore_db_from_dump('db/dump.sql', cursor2)
except Exception:
    print('db already restored')

# fill current_db by new data
for t in TABLES:
    update_db_data(t, conn, cursor, is_initial_insert)


# compare current_data with dump
def test_ship_params():
    cursor.execute(ship_info_sql_template)
    cursor2.execute(ship_info_sql_template)

    current_ship_params = cursor.fetchall()
    dump_ship_params = cursor2.fetchall()
    fields_ = ('weapon', 'hull', 'engine')

    for c in current_ship_params:
        for d in dump_ship_params:
            if c[t.key_field] == d[t.key_field]:
                parts_diff = [
                    '{k} expected {d} was {c}\n'.format(
                        k=k, d=d[k], c=c[k]
                    )
                    for k in c if c[k] != d[k]
                ]
                s = ''.join(parts_diff)
                for f in fields_:
                    yield check_params, c, d, f, s


def check_params(
        current_ship_params,
        dump_ship_params,
        field,
        parts_diff
):
    assert (
            current_ship_params[field] == dump_ship_params[field]
    ), ("""
        Ship check:
        {ship}, {field}-{current_value}\n
        expected {field}-{dump_value}, 
        was {field}-{current_value}.
        -----
        Parts check:
        {ship}, {field}-{current_value}\n
        {parts}
    """
        ).format(
        ship=current_ship_params['ship'],
        field=field,
        current_value=current_ship_params[field],
        dump_value=dump_ship_params[field],
        parts=parts_diff
    )
