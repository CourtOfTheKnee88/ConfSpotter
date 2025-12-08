# Conference Radar – "ConfSpotter"

# IF LOOKING FOR LATEST VERION SEE PHASE III READ ME

Problem: Academic researchers miss important conferences and publication opportunities due
to poor information aggregation. This project informs students and faculty about upcoming
conferences and their deadlines.
Suggested Key Features:

- Personalized conference recommendations
- CFP deadline tracking and notifications
- Submission management system
- Conference networking and attendee matching
- Publication outcome tracking

Team Leader - Courtney Jackson (Courtney.Jackson@maine.edu) (CourtOfTheKnee88) \
Esther Greene (esther.greene@maine.edu) (esthergreene), \
Samuel Fickett (Samuel.Fickett@maine.edu) (SamFickett), \
Seth Tedder (Seth.Tedder@maine.edu) (Seth-Tedder) \
Google Drive: https://docs.google.com/document/d/17Stc62MJ4LH-gEOT_NdcwDbSWMRVzchYqExX04Cgea0/edit?usp=sharing

# Task Assignment and Planning

## Recorded Video Demonstration

**DUE NOVEMBER 14TH 11:59 PM**\
Sam - Record segment about web scraping and cleaning results\
Esther - Record segment about triggers and indexing\
Seth - Record segment about stored procedures, functions and queries\
Courtney - Record segment showing the database running on a screen explaining creation, data loading, and constraints\

## MySQL Database Schema Scripts

**DUE NOVEMBER 4TH 11:00 AM**\
Everyone is responsible for creating the table for their given entity\
Conference Entity - Sam\
User Entity - Seth\
Location Entity - Esther\
Paper Entity - Courtney\
Python Script connecting the database - Courtney\
\
**DUE NOVEMEBER 11TH 11:00 AM**\
Indexing Scprits - Esther \

- Script to speed up lookups when searching by email
- Script to help filter users by interests in queries
- Script to be useful for filtering or joining by geographic region
- Scripts to improve searches for conferences, title, or keywords

Indexing Scripts - Courtney

- Script to speed joins between `Conferences` and `Location`
- Script to filter by paper topics
- Script to speed joins between `papers` and `conferences`
- Script to filter by submission dates
- SQL script to automatically calculate duration

## Stored Procedures and Functions

**DUE NOVEMEBR 14TH 11:00 AM**\
Scripts implementing key system operations - ALL MEMEMBERS

- Script to find personalized conference recommendations
- Script notifies users about paper deadlines for that conference based on paper interests
- Stored Procedures

## Data Scraping Scripts and Documentation

**DUE NOVEMEBR 10TH 11:00 AM**\
Write a python script to scarp data from these 3 websites:

1. [ACM](https://www.acm.org/conferences)
2. [SIGCHI](https://sigchi.org/conferences/)
3. [CIS.IEEE](https://cis.ieee.org/conferences/conference-calendar)

Sam \

Python web scrapping script to scrap papers - Courtney

## Sample Data and Data Cleaning Documentation

**DUE NOVEMEBR 11TH 11:00 AM**\
Data cleaning and normalization for conferences - Courtney
Data cleaning and normalization for papers - Sam

**DUE NOVEMEBR 12TH 11:00 AM**\
Create scripts and/or CSV files for sample data inserts - Seth

## Query Optimization Analysis

**DUE NOVEMEBR 14TH 11:59 PM**\
Write a document explaining the indexing strategies - Esther\
Results of before and after query perfromances results for 2 queries - Seth

# Comprehensive README File

**DUE NOVEMEBER 14th 11:59 PM**\
Maintain and update github project and assigning of tasks - Courtney\
Write how to run and how to recreate database - Courtney, Esther, Seth\
How to run web scraping - Sam

# PHASE II:

Location Table:
The Location table stores physical address information for each conference. It includes validation constraints, primary key (LID),
and indexing for efficient lookups by city/state and zip. The table is linked to Conferences via a foreign key relationship (LID).

# HOW TO RUN THE DATABASE:

For MacOS:
`mysql -u ConfSpotter -pchickenlittle < /directorytotheproject/ConfSpotter/SQL/shell.sql`

For Windows:
`mysql -u ConfSpotter -pchickenlittle < "C:\Users\Your Name\Documents\GitHub\ConfSpotter\SQL\shell.sql"`

or if you know you are in the correct directory

`mysql -u ConfSpotter -pchickenlittle < SQL/shell.sql`

To load sample data:
`mysql -u ConfSpotter -pchickenlittle < SQL/sample_project_data.sql`

To load Web Scraping Data:
`python3 "Python/Scraping V3.py"`

To clean the data:
`python3 "Python/clean_conference_data.py"`

To scrap paper deadlines and clean them:
`python3 "Python/PaperScrapping.py"`

To Convert to CSV and import into database:
`python3 "Python/csv-conversion-script.py"`

# Web Scraping Steps

If the following packages aren't already installed, please install them:

- requests
- pandas
- beautifulsoup4
- re
- urllib.parse

Once all packages are installed to python, all you need to do is run the program.
