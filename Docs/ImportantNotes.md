When you set up a project you need to run the SQL file first. Then you can run the python script.

Before running SQL make sure you have:

- mysql.connector

For MacOS:
`mysql -u ConfSpotter -pchickenlittle < /directorytotheproject/ConfSpotter/SQL/shell.sql`

or if you know you are in the correct directory

`mysql -u ConfSpotter -pchickenlittle < SQL/shell.sql`

For Windows:
`mysql -u ConfSpotter -pchickenlittle < "C:\Users\Your Name\Documents\GitHub\ConfSpotter\SQL\shell.sql"`

To check if it is actually running:
`mysql -u ConfSpotter -pchickenlittle -e "USE confspotter; SHOW TABLES;"`

To load sample data:
`mysql -u ConfSpotter -pchickenlittle < SQL/sample_project_data.sql`

Before Running Web Scrapping Ensure that these packages are installed:

- requests
- pandas
- beautifulsoup4
- re
- urllib.parse

To load Web Scraping Data:
`python3 "Python/Scraping V3.py"`

To clean the data:
`python3 "Python/clean_conference_data.py"`

To scrap paper deadlines and clean them:
`python3 "Python/PaperScrapping.py"`

To Convert to CSV and import into database:
`python3 "Python/csv-conversion-script.py"`

To Run the Stored Procedures and Triggers:
`mysql -u ConfSpotter -pchickenlittle confspotter < "SQL/Stored_Procedures and Triggers.sql"`

To View Data in Tables:

View all conferences:
`mysql -u ConfSpotter -pchickenlittle -e "USE confspotter; SELECT * FROM Conferences;"`

View all papers:
`mysql -u ConfSpotter -pchickenlittle -e "USE confspotter; SELECT * FROM Papers;"`

View all users:
`mysql -u ConfSpotter -pchickenlittle -e "USE confspotter; SELECT * FROM user;"`

View all locations:
`mysql -u ConfSpotter -pchickenlittle -e "USE confspotter; SELECT * FROM Location;"`

Count rows in each table:
`mysql -u ConfSpotter -pchickenlittle -e "USE confspotter; SELECT 'Conferences' as Table_Name, COUNT(*) as Row_Count FROM Conferences UNION SELECT 'Papers', COUNT(*) FROM Papers UNION SELECT 'Users', COUNT(*) FROM user UNION SELECT 'Locations', COUNT(*) FROM Location;"`

Interactive MySQL session:
`mysql -u ConfSpotter -pchickenlittle confspotter`

Sample Constraint Violation:
INSERT INTO Location (Street_Address, City, State, Zip, Country)
VALUES ('123 Main St', 'Boston', 'MA', '!@#$%', 'USA');

To drop all the tables:
`mysql -u ConfSpotter -pchickenlittle -e "USE confspotter; SET FOREIGN_KEY_CHECKS = 0; DROP TABLE IF EXISTS Papers; DROP TABLE IF EXISTS Conferences; DROP TABLE IF EXISTS user; DROP TABLE IF EXISTS Location; SET FOREIGN_KEY_CHECKS = 1;"`
