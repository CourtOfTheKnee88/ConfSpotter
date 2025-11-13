# author: Seth Tedder
# results prior to indexing -- Execution Time: 0.0 seconds
# results after indexing -- Execution Time: 0.0 seconds

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

query = ("SELECT username, City FROM user, Location WHERE (user.Interest_1 = 'Ethics' OR user.Interest_2 = 'Ethics' OR user.Interest_3 = 'Ethics') AND Location.Zip = 04401")

start = time.time()
cursor.execute(query)
results = cursor.fetchall() 
print(results)
end = time.time()

print("Execution Time:", end - start, "seconds")

connection.close()