import psycopg2

def remove_location(location_id):
    db = None
    curr = None

    try:
        location_id = int(location_id)
    except Exception as e:
        return(f"Invalid location_id {location_id}")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        # Check to see if there are spaceships at this location. If there are,
        # We cannot delete the location
        curr.execute(f"""select s.name from spaceships s
                         join locations l on l.id = s.ship_location
                         where l.id = {location_id};""")
        name = curr.fetchall()

        if (len(name) < 1):
            return "Error deleting location: There are still spaceShips at this location"

        curr.execute(f"""select city_name
                         from locations
                         where id = {location_id};""")
        name = curr.fetchall()

        # remove spaceship from db
        curr.execute(f"delete from locations where id = {location_id};")

        db.commit()

        return (f"""Successfully removed the location {name[0][0]}""")

    except psycopg2.Error as err:
        return f"Error deleting location;    " + str(err)
    finally:
        if db:
            db.close()
        if curr:
            curr.close()