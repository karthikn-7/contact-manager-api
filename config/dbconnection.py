from pymongo import MongoClient
from dotenv import load_dotenv
import os


def dbconnection():
    load_dotenv("../")
    conn_string = os.getenv("DB_CONN_STRING")
    try:
        client = MongoClient(conn_string)
        print("Database connected")
        return client
    except Exception as ex:
        print(ex)
