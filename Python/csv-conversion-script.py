# author: Seth Tedder
# some variables will have to be altered for the final system or for universality.
# No code was copied directly from ChatGPT or any other LLM, though AI was used to determine how the code should function.

import random
import string
import csv
import mysql.connector

#connects to database.
connection = mysql.connector.connect(       # Replace values with those that match your database.
    host='localhost', user='ConfSpotter', password='chickenlittle', database='confspotter') 

#facilitates interaction with the database.
cursor = connection.cursor()

# Conferences
# Accesses csv file and adds all valid lines to database
with open('conferences_normalized.csv', newline='') as data1:
    reader1 = csv.DictReader(data1)
    for x in reader1:
        if all(x.values()):
            print(x)
            # This line was sourced from stackoverflow with modifications at:
            # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits 
            cursor.execute("INSERT INTO Conferences (Title, Start_Date, End_Date, Descrip, link) VALUES (%s, %s, %s, %s, %s)",
                           (x['name'], x['start_date'], x['end_date'], x['location'][:99], x['link']))

# Commit conferences first so we can reference them
connection.commit()
            
# Papers
with open('papers_cleaned.csv', newline='') as data2:
    reader2 = csv.DictReader(data2)
    for y in reader2:
        if all(y.values()):
            print(y)
            # This line was sourced from stackoverflow with modifications at:
            # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits 
            # Look up the CID based on conference title
            cursor.execute("SELECT CID FROM Conferences WHERE Title = %s", (y['conference_title'],))
            result = cursor.fetchone()
            cid = result[0] if result else None
            
            cursor.execute("INSERT INTO Papers (TypeOfPaper, Topic, DueDate, CID) VALUES (%s, %s, %s, %s)",
                           (y['type'][:50], y['conference_title'][:100], y['deadline'], cid))
            

connection.commit()
connection.close()