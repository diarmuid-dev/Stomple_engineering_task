import psycopg2

def remove_spaceship(ship_id):
    db = None
    curr = None

    try:
        ship_id = int(ship_id)
    except Exception as e:
        return(f"Invalid ship_id {ship_id}")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        # get name of spaceship before it is removed
        curr.execute(f"select name from spaceships where id = {ship_id};")
        name = curr.fetchall()

        # remove spaceship from db
        curr.execute(f"delete from spaceships where id = {ship_id};")

        db.commit()

        return (f"""Successfully removed the spaceship {name[0][0]}""")

    except psycopg2.Error as err:
        return f"Spaceship {ship_id} does not exist"
    finally:
        if db:
            db.close()
        if curr:
            curr.close()