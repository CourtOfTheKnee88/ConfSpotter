# author: Seth Tedder
# some variables will have to be altered for the final system or for universality.
# No code was copied directly from ChatGPT or any other LLM, though AI was used to determine how the code should function.

import random
import string
import csv
import mysql.connector

#connects to database.
connection = mysql.connector.connect(       # Replace values with those that match your database.
    host='localhost', port=3306, user='root', password='chickenlittle', database='confspotter') 

#facilitates interaction with the database.
cursor = connection.cursor()

# Accesses csv file and adds all valid lines to database
with open('conferences_normalized.csv', newline='') as data:
    reader = csv.DictReader(data)
    for x in reader:
        if all(x.values()):
            print(x)
            cursor.execute("INSERT INTO Conferences (CID, Title, State_Date, End_Date, Descrip) VALUES (%s, %s, %s, %s, %s)",
                           # This line was sourced from stackoverflow at:
                           # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits 
                           (''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6)),
                            x['name'], x['start_date'], x['end_date'], x['location'][:99]))
connection.commit()
connection.close()
