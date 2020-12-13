import psycopg2
from utils import locationExists, shipExists

def travel_ship(ship_id, location_id):
    db = None
    curr = None

    try:
        ship_id = int(ship_id)
    except Exception as e:
        return(f"Invalid ship id {ship_id}")

    try:
        location_id = int(location_id)
    except Exception as e:
        return(f"Invalid ship id {location_id}")


    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        if (not locationExists(curr, location_id)):
            return 'The space port with id ' + str(location_id) + ' does not exist'

        curr.execute(f"""select space_port_capacity, city_name, planet_name 
                            from locations where id = {location_id}""")

        capacity, city, planet = curr.fetchone()

        curr.execute(f"""select count(*) from spaceships 
                        where ship_location = {location_id}""")

        numShips = curr.fetchone()[0]

        if (not shipExists(curr, ship_id)):
            return 'The spaceship with id ' + str(ship_id) + ' does not exist'

        curr.execute(f"""select name from spaceships where id = {ship_id}""")

        shipname = curr.fetchone()[0]

        if (numShips + 1 <= capacity):
            curr.execute(f"""update spaceships
                            set ship_location = {ship_id}
                            where id = {location_id}""")
            db.commit()
            return 'Successfuly moved ship ' +  shipname +  ' to ' +  city +  ', ' +  planet
        else:
            return 'The space port at ' +  city +  ', ' +  planet +  ' is at capacity'

    except psycopg2.Error as err:
        print ("ERROR" + str(err))
        return str(err)
    finally:
        if db:
            db.close()
        if curr:
            curr.close()