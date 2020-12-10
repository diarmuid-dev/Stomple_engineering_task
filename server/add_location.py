import psycopg2

def add_location(city, planet, capacity):
    db = None
    cur = None

    if (city == '' or planet == ''):
        return ("The city or plannet cannot be null")

    try:
        capacity = int(capacity)
    except exception as e:
        return(f"Invalid year {capacity}")

    try:
        db = psycopg2.connect("dbname=stomple")
        curr = db.cursor()

        # Insert new location into db
        curr.execute(f"insert into location values (default, %s, %s, {capacity});",
                        [city, planet])

        db.commit()

        return (f"""Successfully added the location {city} on planet {planet} with capacity {capacity}""")

    except psycopg2.Error as err:
        return "Failed to insert"
    finally:
        if db:
            db.close()
        if cur:
            cur.close()