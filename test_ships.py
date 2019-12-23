from sqlalchemy import create_engine
from sqlalchemy.sql import text

from .fill_db import (
    is_initial_insert,
    restore_from_dump,
    insert_data,
    make_dump,
    update_data
)

from .models import (
    weapons,
    hulls,
    engines,
    ships
)
from .sql_templates import ship_info_sql_template

TABLES = (weapons, hulls, engines, ships)

engine_current = create_engine('sqlite:///db/test.db', echo=True)
engine_dump = create_engine('sqlite:///db/dump.db', echo=True)

conn_dump_raw = engine_dump.raw_connection()
conn_dump = engine_dump.connect()
cursor_dump = conn_dump_raw.cursor()

conn_current = engine_current.connect()
conn_current_raw = engine_current.raw_connection()
cursor_current = conn_current_raw.cursor()

number_of_rows = {
    'weapons': 21,
    'hulls': 6,
    'engines': 7,
    'ships': 201
}

initial_insert = is_initial_insert(cursor_current)

if initial_insert:
    restore_from_dump('db/init_db.sql', cursor_current)


for t in TABLES:
    insert_data(t, conn_current, number_of_rows[t.name])

make_dump(conn_current_raw)

try:
    restore_from_dump('db/dump.sql', cursor_dump)
except Exception:
    print('db restored')

for t in TABLES:
    update_data(t, conn_current, number_of_rows[t.name])


# compare current_data with dump
def test_ship_params():
    txt = text(ship_info_sql_template)
    current_ship_params = conn_current.execute(txt).fetchall()
    dump_ship_params = conn_dump.execute(txt).fetchall()

    fields_ = ('weapon', 'hull', 'engine')

    for current in current_ship_params:
        for dump in dump_ship_params:
            if current.ship == dump.ship:
                parts_diff = [
                    '\t"{field}": expected {dump}, was {current}\n'.format(
                        field=c_field,
                        dump=dump[c_field],
                        current=current[c_field]
                    )
                    for c_field in current.keys()
                    if current[c_field] != dump[c_field]
                ]
                params_difference = ''.join(parts_diff)
                for field in fields_:
                    yield check_params, current, dump, field, params_difference


def check_params(
        current_ship_params,
        dump_ship_params,
        field,
        parts_diff
):
    assert (
            current_ship_params[field] == dump_ship_params[field]
    ), (
        """
    Ship check:
    {ship}, "{field}"-{current_value}
    \texpected "{field}"-{dump_value}, was "{field}"-{current_value}.
    -----
    Parts check:
    {ship}, "{field}"-{current_value}
{parts}
    """
    ).format(
        ship=current_ship_params['ship'],
        field=field,
        current_value=current_ship_params[field],
        dump_value=dump_ship_params[field],
        parts=parts_diff
    )


def teardown():
    for t in TABLES:
        t.drop(conn_current)
        t.drop(conn_dump)
