import psycopg2
from utils import shipExists, isInt

def remove_spaceship(ship_id):
    db = None
    curr = None

    if (not isInt(ship_id)):
        return(f"(0, Invalid ship_id {ship_id})")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        if (not shipExists(curr, ship_id)):
            return f"(0, Spaceship {ship_id} does not exist)"

        # get name of spaceship before it is removed
        curr.execute(f"select name from spaceships where id = {ship_id};")
        name = curr.fetchall()

        # remove spaceship from db
        curr.execute(f"delete from spaceships where id = {ship_id};")

        db.commit()

        return (f"""(1, Successfully removed the spaceship {name[0][0]})""")

    except psycopg2.Error as err:
        return f"(0, Failed to delete: {str(err)})"
    finally:
        if db:
            db.close()
        if curr:
            curr.close()