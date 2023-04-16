import sqlite3
from sqlite3 import Error
import logging
import aiosqlite
import asyncio

PATH = '..\..\Database\IoTDatabase'
TABLE_NAME = 'profile'
current_user_data = []

def create_connection(a):
    # global connection
    connection = None
    try:
        connection = aiosqlite.connect(PATH)
        print("Database connection is successful")

    except Error as e:
        print(f"The error '{e} occured'")

    return connection


async def read() -> list:
    global current_user_data
    logging.basicConfig(level=logging.INFO)
    async with aiosqlite.connect(PATH) as db, db.execute("SELECt * FROM profile") as cursor:
        current_user_data = await cursor.fetchall()


if __name__ == "__main__":
    asyncio.run(read())

