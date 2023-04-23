import sqlite3
from sqlite3 import Error
import logging
import aiosqlite
import asyncio

connection = None
current_user_data = None
USER_LOGGED = False

# Sync
def sync_create_connection(PATH) -> sqlite3.Connection :
    global  connection
    #PATH = '..\..\Database\IoTDatabase'
    try:
        connection = sqlite3.connect(PATH, check_same_thread=False)
        print("Database connection is successful")
    except Error as e:
        print(f"The error '{e} occured'")

    return connection


def sync_getAll(connection : sqlite3.Connection):
    cur = connection.cursor()
    cur.execute("SELECT * FROM profile")
    rows = cur.fetchall()
    for row in rows:
        print(row)

"""
@PARAMS (sqlite.Cconnection, id : str)
@RETURN list
DESC: return user from the database base on the ID given
"""
def sync_getProfileById(connection : sqlite3.Connection, id : str) -> list:
    global  current_user_data
    cur = connection.cursor()
    cur.execute("SELECT * FROM profile WHERE id=?",(id,))
    current_user_data = cur.fetchone()
    return  current_user_data if current_user_data is not None else []


# async
async def asyncRead(PATH, id) -> list:
    global current_user_data
    logging.basicConfig(level=logging.INFO)
    async with aiosqlite.connect(PATH) as db, db.execute("SELECt * FROM profile WHERE id=?",(id,)) as cursor:
        current_user_data = await cursor.fetchone()



if __name__ == "__main__":
    #asyncio.run(read())
    PATH = '..\..\Database\IoTDatabase.db'
    con = sync_create_connection(PATH)
    sync_read(con)

