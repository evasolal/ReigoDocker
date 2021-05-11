import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
'''
    finally:
        if conn:
            conn.close()
'''
#Create an address entrie
def create_address(conn, prop):
    sql = '''INSERT OR REPLACE INTO address(ADDRESS,BEDROOMS, BATHROOMS,SIZE, SOLD_ON,ZESTIMATE,WALK_SCORE,TRANSIT_SCORE,GREAT_SCHOOLS)
            VALUES(?,?,?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql,prop)
    conn.commit()
    return cur.lastrowid

#Add the entrie to our database
def add_entrie(lst):
    conn = create_connection("resources/addresses.db")
    with conn:
        prop = tuple(lst)
        prop_id = create_address(conn, prop)


