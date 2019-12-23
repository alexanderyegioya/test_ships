import sqlite3
import time
from random import randint

from sqlalchemy import create_engine, update, bindparam
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker

metadata = MetaData()
weapons = Table(
    'weapons', metadata,
    Column('id', Integer, primary_key=True),
    Column('weapon', String),
    Column('reload_speed', Integer),
    Column('rotational_speed', Integer),
    Column('diameter', Integer),
    Column('power_volley', Integer),
    Column('count', Integer),
)

hulls = Table(
    'hulls', metadata,
    Column('id', Integer, primary_key=True),
    Column('hull', String),
    Column('armor', Integer),
    Column('type', Integer),
    Column('capacity', Integer),
)

engines = Table(
    'engines', metadata,
    Column('id', Integer, primary_key=True),
    Column('engine', String),
    Column('power', Integer),
    Column('type', Integer),
)

ships = Table(
    'ships', metadata,
    Column('id', Integer, primary_key=True),
    Column('ship', String),
    Column('weapon', ForeignKey(weapons.c.id)),
    Column('hull', ForeignKey(hulls.c.id)),
    Column('engine', ForeignKey(engines.c.id)),
)


class Weapon():
    def __init__(
            self,
            weapon,
            reload_speed,
            rotational_speed,
            diameter,
            power_volley,
            count
    ):
        self.weapon = weapon
        self.reload_speed = reload_speed
        self.rotational_speed = rotational_speed
        self.diameter = diameter
        self.power_volley = power_volley
        self.count = count

    def __repr__(self):
        return "<Weapon('%s')>" % (self.weapon)


class Hull():
    def __init__(
            self,
            hull,
            armor,
            type,
            capacity
    ):
        self.hull = hull,
        self.armor = armor
        self.type = type
        self.capacity = capacity

    def __repr__(self):
        return "<Hull('%s')>" % (self.hull)


class Engine():
    def __init__(
            self,
            engine,
            power,
            type
    ):
        self.engine = engine,
        self.power = power
        self.type = type

    def __repr__(self):
        return "<Engine('%s')>" % (self.engine)


class Ship():
    def __init__(
            self,
            ship,
            weapon,
            hull,
            engine
    ):
        self.ship = ship,
        self.engine = engine,
        self.hull = hull
        self.weapon = weapon

    def __repr__(self):
        return "<Ship('%s')>" % (self.ship)
