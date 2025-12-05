import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "ConfSpotter"),
            port=os.getenv("DB_PORT", "3306"),
            password=os.getenv("DB_PASSWORD", "chickenlittle"),
            database=os.getenv("DB_NAME", "confspotter"),
            autocommit=True,
        )
        return conn
    except Error:
        raise
