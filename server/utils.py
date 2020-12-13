import psycopg2

def shipExists(curr, ship_id):
    curr.execute(f'select * from spaceships where id = {ship_id}')
    if (len(curr.fetchall()) > 0):
        return True
    
    return False

def locationExists(curr, location_id):
    curr.execute(f'select * from locations where id = {location_id}')
    if (len(curr.fetchall()) > 0):
        return True
    
    return False
