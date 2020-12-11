import psycopg2

def add_spaceship(name, model, status, location):
    db = None
    curr = None

    # enforce null constraints. status constraints enforced at db level
    if (name == '' or model == '' or status == ''):
        return ("The name, model or status cannot be null")

    try:
        location = int(location)
    except Exception as e:
        return(f"Invalid location {location}")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        # Insert new spaceship into db
        curr.execute(f"insert into spaceships values (default, %s, %s, %s, {location});",
                        [name, model, status])

        db.commit()

        return (f"""Successfully added the spaceship {name}""")

    except psycopg2.Error as err:
        return "Failed to insert"
    finally:
        if db:
            db.close()
        if curr:
            curr.close()