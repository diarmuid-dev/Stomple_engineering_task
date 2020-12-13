import psycopg2
from utils import locationExists, isInt

def add_location(location_id, city, planet, capacity):
    db = None
    curr = None

    # ensure city and planet are not null
    if (city == '' or planet == ''):
        return ("The city or plannet cannot be null")

    # Check data validity
    if (not isInt(capacity)):
        return(f"Invalid capacity {capacity}. Must be an integer")

    if (not isInt(location_id)):
        return(f"Invalid location {location_id}. Must be an integer")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()


        if (locationExists(curr, location_id)):
            return f'Location with id {location_id} already exists'

        # Insert new location into db
        curr.execute(f"insert into locations values ({location_id}, %s, %s, {capacity});",
                        [city, planet])

        # Commit to database
        db.commit()

        return (f"""Successfully added the location {city} on planet {planet} with capacity {capacity} and id {location_id}""")

    except psycopg2.Error as err:
        if ('capacityConstraint' in str(err)):
            return 'Error: Invalid space_port_capacity'
        elif ('null' in str(err)):
            return 'No input values can be null'
        else:
            return f"Failed to insert: {str(err)}"
    finally:
        if db:
            db.close()
        if curr:
            curr.close()