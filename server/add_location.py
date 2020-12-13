import psycopg2
from utils import locationExists, isInt

def add_location(location_id, city, planet, capacity):
    db = None
    curr = None

    # ensure city and planet are not null
    if (city == '' or planet == ''):
        return (f"(0, The city or plannet cannot be null)")

    # Check data validity
    if (not isInt(capacity)):
        return(f"(0, Invalid capacity {capacity}. Must be an integer)")

    if (not isInt(location_id)):
        return(f"(0, Invalid location {location_id}. Must be an integer)")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()


        if (locationExists(curr, location_id)):
            return f"(0, Location with id {location_id} already exists)"

        # Insert new location into db
        curr.execute(f"insert into locations values ({location_id}, %s, %s, {capacity});",
                        [city, planet])

        # Commit to database
        db.commit()

        return (f"(1, Successfully added the location {city} on planet {planet} with capacity {capacity} and id {location_id})")

    except psycopg2.Error as err:
        if ('capacityConstraint' in str(err)):
            return f"(0, Error: Invalid space_port_capacity)"
        elif ('null' in str(err)):
            return f"(0, No input values can be null)"
        else:
            return f"Failed to insert: {str(err)}"
    finally:
        if db:
            db.close()
        if curr:
            curr.close()