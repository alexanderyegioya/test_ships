import os
import sqlite3

from fill_db import TABLES, restore_db_from_dump, fill_db_with_data

CURRENT_DB = os.path.join(os.path.dirname(__file__), 'db/ships.db')
DUMP_DB = os.path.join(os.path.dirname(__file__), 'db/dump.db')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def make_dump(conn):
    with open('db/dump.sql', 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)


conn = sqlite3.connect(CURRENT_DB)
make_dump(conn)

conn.row_factory = dict_factory
cursor = conn.cursor()

conn2 = sqlite3.connect(DUMP_DB)
conn2.row_factory = dict_factory
cursor2 = conn2.cursor()

try:
    restore_db_from_dump('db/dump.sql', cursor2)
except Exception:
    print('db already restored')

for t in TABLES:
    fill_db_with_data(t, conn, cursor)


def test_ship_params():
    for t in TABLES:
        cursor.execute('select * from {table_name}'.format(table_name=t.table_name))
        cursor2.execute('select * from {table_name}'.format(table_name=t.table_name))

        current_ship_params = cursor.fetchall()
        dump_ship_params = cursor2.fetchall()

        for c in current_ship_params:
            for d in dump_ship_params:
                if c[t.key_field] == d[t.key_field]:
                    for f in t.fields:
                        yield check_params, c, d, f


def check_params(current_weapon, dump_weapon, field):
    assert current_weapon[field] == dump_weapon[field]
