import psycopg2

def update_ship_status(ship_id, status):
    db = None
    curr = None

    if (status == ''):
        return ("The status cannot be null")

    try:
        ship_id = int(ship_id)
    except exception as e:
        return(f"Invalid year {ship_id}")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        # Insert new location into db
        curr.execute(f"update spaceships set status = '{status}' where id = {ship_id};")

        db.commit()

        curr.execute(f"select name from spaceships where id = {ship_id};")

        name = curr.fetchall()

        return (f"Successfully updated {name[0][0]} to {status}")

    except psycopg2.Error as err:
        print ("ERROR" + str(err))
        return err
    finally:
        if db:
            db.close()
        if curr:
            curr.close()