ship_info_sql_template = """
    SELECT
        s.ship,
        s.weapon,
        s.hull,
        s.engine,
        w.reload_speed,
        w.rotational_speed,
        w.diameter,
        w.power_volley,
        w.count,
        h.armor,
        h.type,
        h.capacity,
        e.power,
        e.type
    FROM ships s
    LEFT JOIN weapons w ON s.weapon=w.ROWID
    LEFT JOIN hulls h ON s.hull=h.ROWID
    LEFT JOIN engines e ON s.engine=e.ROWID;            
"""

all_tables_sql = """
    SELECT name from sqlite_master where type= "table"
"""