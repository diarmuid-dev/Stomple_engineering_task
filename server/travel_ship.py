import psycopg2

def travel_ship(ship_id, location_id):
    db = None
    curr = None

    try:
        ship_id = int(ship_id)
    except Exception as e:
        return(f"Invalid year {ship_id}")

    try:
        location_id = int(location_id)
    except Exception as e:
        return(f"Invalid year {location_id}")


    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        # Insert new location into db
        curr.execute(f"""select * from moveship({ship_id},{location_id});""")

        

        curr.execute(f"""select s.name, l.city_name, l.planet_name 
                         from spaceships s 
                         join locations l on l.id = s.ship_location
                         where id = {ship_id};""")

        name, location = curr.fetchall()

        db.commit()

        return (f"Successfully updated {name[0][0]} to {status}")

    except psycopg2.Error as err:
        print ("ERROR" + str(err))
        return str(err)
    finally:
        if db:
            db.close()
        if curr:
            curr.close()