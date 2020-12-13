import psycopg2
from utils import isInt, shipExists

def update_ship_status(ship_id, status):
    db = None
    curr = None

    if (status == ''):
        return ("(0, The status cannot be null)")

    if (not isInt(ship_id)):
        return(f"(0, Invalid year {ship_id}. Must be an integer)")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        if (not shipExists(curr, ship_id)):
            return f"(0, Spaceship {ship_id} does not exist)"

        curr.execute(f"select name from spaceships where id = {ship_id};")

        name = curr.fetchone()

        # Insert new location into db
        curr.execute(f"update spaceships set status = '{status}' where id = {ship_id};")

        db.commit()

        return (f"(1, Successfully updated {name[0]} to {status})")

    except psycopg2.Error as err:
        print ("ERROR" + str(err))
        if ('status_constraint' in str(err)):
            return '(0, Error: Invalid Status)'
        else:
            return str(err)
    finally:
        if db:
            db.close()
        if curr:
            curr.close()