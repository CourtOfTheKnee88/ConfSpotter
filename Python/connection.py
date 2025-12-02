import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="ConfSpotter",
            port="3306",
            password="chickenlittle",
            database="confspotter",
            autocommit=True,
        )
        return conn
    except Error:
        raise
