create table location(
    id serial primary key,
    city_name text not null,
    planet_name text not null,
    space_port_capacity integer not null
);

create table spaceship(
    id serial primary key,
    name text not null,
    model text not null,
    ship_location integer not null,

    foreign key (ship_location) references location(id),

    status text not null check (
        status in ('decommissioned', 'maintenance', 'operational'))
);