import psycopg2
from utils import locationExists, shipExists, isInt

def travel_ship(ship_id, location_id):
    db = None
    curr = None



    if (not isInt(ship_id)):
        return(f"Invalid ship id {ship_id}")


    if (not isInt(location_id)):
        return(f"Invalid ship id {location_id}")


    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        # Check that the location exists
        if (not locationExists(curr, location_id)):
            return 'The space port with id ' + str(location_id) + ' does not exist'

        curr.execute(f"""select space_port_capacity, city_name, planet_name 
                            from locations where id = {location_id}""")

        capacity, city, planet = curr.fetchone()

        curr.execute(f"""select count(*) from spaceships 
                        where ship_location = {location_id}""")

        # Check that the spaceship exists
        numShips = curr.fetchone()[0]

        if (not shipExists(curr, ship_id)):
            return 'The spaceship with id ' + str(ship_id) + ' does not exist'

        # Ship can only travel if operational, therefore we need to check
        curr.execute(f"""select name, status from spaceships where id = {ship_id}""")
        
        shipname, status = curr.fetchone()

        if (not status == 'operational'):
            return f'The ship {shipname} has the status {status}'

        # Check that the spaceport at location_id is not at capacity
        if (numShips + 1 <= capacity):
            # update ships location
            curr.execute(f"""update spaceships
                            set ship_location = {location_id}
                            where id = {ship_id}""")
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