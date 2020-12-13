create table locations(
    id serial primary key,
    -- it does not make sense to have two ports at the same city, as we cannot
    -- differentiate between them in this schema. Hence, the city is unique
    city_name text unique not null,
    planet_name text not null,
    space_port_capacity integer not null,

    constraint capacityConstraint check (
        space_port_capacity > 0
    )
);

create table spaceships(
    id serial primary key,
    name text not null,
    model text not null,
    status text not null,
    -- Ships must be at a port at all times
    ship_location integer not null,

    foreign key (ship_location) references locations(id),

    constraint status_constraint check (
        status in ('decommissioned', 'maintenance', 'operational'))
);