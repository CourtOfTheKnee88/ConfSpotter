import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="ConfSpotter",
            password="chickenlittle",
            database="confspotter",
            autocommit=True,
        )
        return conn
    except Error:
        raise
