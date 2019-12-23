from random import randint

from .models import hulls, weapons, engines, ships
from .sql_templates import all_tables_sql


def restore_from_dump(dump_filename, cursor):
    with open(dump_filename, 'r') as f:
        sql = f.read()
        cursor.executescript(sql)


TABLES = (
    hulls,
    weapons,
    engines,
    ships,
)


def make_dump(conn):
    conn.row_factory = None
    with open('db/dump.sql', 'w') as f:
        f.truncate()
        for line in conn.iterdump():
            f.write('%s\n' % line)


def update_key_field(row_number, row, key_field):
    row.update(
        {
            key_field: '{item_name}-{order_number}'.format(
                item_name=key_field.capitalize(),
                order_number=row_number
            )
        }
    )


def generate_values_for_query(
        table_details,
        number_of_rows_to_insert,
        key_field,
        excluded_fields,
        is_update_query
):
    if is_update_query:
        table_data = [
            {
                str(field.name): randint(
                    i, 100
                ) for field in table_details.columns if (
                    len(str(field.name)) % randint(2, 3) == 0 and
                    str(field.name) not in excluded_fields
                )
            } for i in range(1, number_of_rows_to_insert)
        ]
    else:
        table_data = [
            {
                str(field.name): randint(
                    i, 100
                ) for field in table_details.columns if (
                    str(field.name) not in excluded_fields
                )
            } for i in range(1, number_of_rows_to_insert)
        ]

        for row_number, row in enumerate(table_data):
            update_key_field(row_number, row, key_field)

    return tuple(table_data)


def generate_values_for_ships_query(
        number_rows_to_insert,
        key_field,
        is_update_query
):
    table_data = []

    values_range = {
        'weapon': (1, 19),
        'hull': (1, 4),
        'engine': (1, 5)
    }

    if is_update_query:
        for i in range(1, number_rows_to_insert):
            f = {}
            field = list(values_range.keys())[randint(0, 2)]
            f[field] = randint(*values_range[field])
            table_data.append(f)
    else:
        for i in range(1, number_rows_to_insert):
            f = {}
            for v in values_range:
                f[v] = randint(*values_range[v])
            table_data.append(f)

        for row_number, row in enumerate(table_data):
            update_key_field(row_number, row, key_field)

    return tuple(table_data)


def get_key_field(table_details):
    return table_details.c[
        table_details.name.rstrip('s')
    ].name


def insert_data(
        table_details,
        conn,
        number_of_rows_to_insert
):
    key_field = get_key_field(table_details)
    excluded_fields = [key_field, 'id']

    if table_details.name == 'ships':
        values = generate_values_for_ships_query(
            number_of_rows_to_insert,
            key_field,
            is_update_query=False
        )
    else:
        values = generate_values_for_query(
            table_details,
            number_of_rows_to_insert,
            key_field,
            excluded_fields=excluded_fields,
            is_update_query=False
        )

    ins = table_details.insert()
    conn.execute(ins, values)


def update_data(
        table_details,
        conn,
        number_of_rows_to_insert
):
    key_field = get_key_field(table_details)
    excluded_fields = [key_field, 'id']

    if table_details.name == 'ships':
        values = generate_values_for_ships_query(
            number_of_rows_to_insert,
            key_field,
            is_update_query=True
        )
    else:
        values = generate_values_for_query(
            table_details,
            number_of_rows_to_insert,
            key_field,
            excluded_fields,
            is_update_query=True
        )

    for row_number, v in enumerate(values):
        if v:
            search = "%{}".format(row_number)
            upd = table_details.update().where(
                table_details.c[
                    table_details.name.rstrip('s')
                ].endswith(search)
            ).values(**v)
            conn.execute(upd)


def is_initial_insert(cursor):
    all_tables = cursor.execute(
        all_tables_sql
    ).fetchall()
    try:
        all_tables = set([i[0] for i in all_tables])
    except KeyError:
        return False
    return bool(
        set([i.name for i in TABLES]) - all_tables
    )
