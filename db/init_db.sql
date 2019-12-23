create table weapons(
    weapon text(512), 
    reload_speed integer,
    rotational_speed integer,
    diameter integer,
    power_volley integer,
    count integer
);

create table hulls(
    hull text(512), 
    armor integer,
    type integer,
    capacity integer
);

create table engines(
    engine text(512), 
    power integer,
    type integer
);

create table ships(
    ship text(512),
    weapon text(512), 
    hull text(512),
    engine text(512),
    FOREIGN KEY(weapon) REFERENCES weapons(weapon),
    FOREIGN KEY(hull) REFERENCES hulls(hull),
    FOREIGN KEY(engine) REFERENCES engines(engine)
);
