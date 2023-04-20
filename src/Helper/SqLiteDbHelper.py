import sqlite3
from sqlite3 import Error
import logging
import aiosqlite
import asyncio

PATH = '..\..\Database\IoTDatabase'
TABLE_NAME = 'profile'
current_user_data = []
connection = None

# Sync
def sync_create_connection():
    global connection
    connection = None
    try:
        connection = sqlite3.connect(PATH)
        print("Database connection is successful")

    except Error as e:
        print(f"The error '{e} occured'")

    return connection


def sync_read():
    global connection
    cur = connection.cursor()
    cur.execute("SELECT * FROM profile")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def sync_getProfileById(id):
    pass

# async
async def read() -> list:
    global current_user_data
    logging.basicConfig(level=logging.INFO)
    async with aiosqlite.connect(PATH) as db, db.execute("SELECt * FROM profile") as cursor:
        current_user_data = await cursor.fetchall()


if __name__ == "__main__":
    #asyncio.run(read())
    create_connection()
    sync_read()

