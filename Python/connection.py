import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="ConfSpotter",
    password="chickenlittle",
    database="confspotter"
)

connection.close()
