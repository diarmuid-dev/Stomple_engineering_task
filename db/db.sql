create table locations(
    id serial primary key,
    -- it does not make sense to have two ports at the same city, as we cannot
    -- differentiate between them in this schema. Hence, the city is unique
    city_name text unique not null,
    planet_name text not null,
    space_port_capacity integer not null
);

create table spaceships(
    id serial primary key,
    name text not null,
    model text not null,
    status text not null,
    ship_location integer not null,

    foreign key (ship_location) references locations(id),

    constraint status_constraint check (
        status in ('decommissioned', 'maintenance', 'operational'))
);

create or replace function moveShip(ship_id integer, location_id integer)
    returns text
as $$
DECLARE
    _capacity integer;
    _numShips integer;
    _city text;
    _planet text;
    _shipname text;
begin
    select space_port_capacity, city_name, planet_name 
        into _capacity, _city, _planet 
        from locations 
        where id = location_id;

    if (_city is null) THEN
        return 'The space port with id ' || location_id || ' does not exist'
    end if;

    select count(*) into _numShips from spaceships 
        where ship_location = location_id;

    select name into _shipname from spaceships where id = ship_id;

    if (_shipname is null) THEN
        return 'The spaceship with id ' || ship_id || ' does not exist'
    end if;

    if (_numShips + 1 <= _capacity) then
        update spaceships
        set ship_location = ship_id
        where id = location_id;
        return 'Successfuly moved ship ' || _shipname || ' to ' || _city || 
                ', ' || _planet;
    else
        return 'The space port at ' || _city || ', ' || _planet || ' is at capacity';
    end if;

    return (select ship_location from spaceships where id = ship_id);
end;
$$ language plpgsql;