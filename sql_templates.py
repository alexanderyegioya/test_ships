
weapons_sql_template ="""
    INSERT INTO weapons (
        weapon,
        reload_speed,
        rotational_speed,
        diameter,
        power_volley,
        count
    ) VALUES (
        :weapon,
        :reload_speed,
        :rotational_speed,
        :diameter,
        :power_volley,
        :count
    )
"""

hulls_sql_template ="""
    INSERT INTO hulls (
        hull,
        armor,
        type,
        capacity
    ) VALUES (
        :hull,
        :armor,
        :type,
        :capacity
    )
"""

engines_sql_template ="""
    INSERT INTO engines (
        engine,
        power,
        type
    ) VALUES (
        :engine,
        :power,
        :type
    )
"""

ships_sql_template ="""
    INSERT INTO ships (
        ship,
        weapon,
        hull,
        engine
    ) VALUES (
        :ship,
        :weapon,
        :hull,
        :engine
    )
"""