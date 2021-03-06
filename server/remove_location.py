import psycopg2
from utils import locationExists, isInt

def remove_location(location_id):
    db = None
    curr = None

    if (not isInt(location_id)):
        return(f"Invalid location_id {location_id}")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        if (not locationExists(curr, location_id)):
            return "(0, Error: this location does not exist)"

        # Check to see if there are spaceships at this location. If there are,
        # We cannot delete the location
        curr.execute(f"""select s.name from spaceships s
                         join locations l on l.id = s.ship_location
                         where l.id = {location_id};""")
        name = curr.fetchall()

        if (len(name) > 0):
            return "(0, Error deleting location: There are still spaceShips at this location)"

        curr.execute(f"""select city_name
                         from locations
                         where id = {location_id};""")
        name = curr.fetchone()

        # remove spaceship from db
        curr.execute(f"delete from locations where id = {location_id};")

        db.commit()

        return (f"""(1, Successfully removed the location {name[0]})""")

    except psycopg2.Error as err:
        return f"(0, Error deleting location;    " + str(err) + ')'
    finally:
        if db:
            db.close()
        if curr:
            curr.close()