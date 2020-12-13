import psycopg2
from utils import shipExists, locationExists

def add_spaceship(ship_id, name, model, status, location):
    db = None
    curr = None

    # enforce null constraints. status constraints enforced at db level
    if (name == '' or model == '' or status == ''):
        return ("(0, The name, model or status cannot be null)")

    try:
        location = int(location)
    except Exception as e:
        return(f"Invalid location {location}")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        if (shipExists(curr, ship_id)):
            return f'(0, Spaceship with id {ship_id} already exists)'

        if (not locationExists(curr, location)):
            return f'(0, Location with id {location} does not exist)'

        # Insert new spaceship into db
        curr.execute(f"insert into spaceships values ({ship_id}, %s, %s, %s, {location});",
                        [name, model, status])

        db.commit()

        return (f"""(1, Successfully added the spaceship {name} with id {ship_id})""")

    except psycopg2.Error as err:
        return "(0, Failed to insert: " + str(err) + ')'
    finally:
        if db:
            db.close()
        if curr:
            curr.close()