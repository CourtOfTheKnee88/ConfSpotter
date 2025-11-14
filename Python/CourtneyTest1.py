# author: Courtney Jackson

import mysql.connector
import time

connection = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="1298",
    database="confspotter"
)
cursor = connection.cursor()

query = ("SELECT Title, Descrip, Start_Date, End_Date FROM Conferences WHERE Title LIKE '%AI%' OR Descrip LIKE '%AI%' OR Descrip LIKE '%artificial intelligence%'")

start = time.time()
cursor.execute(query)
results = cursor.fetchall() 
print(results)
end = time.time()

print("Execution Time:", end - start, "seconds")

connection.close()