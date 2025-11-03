# Conference Radar – "ConfSpotter"
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
Indexing Scprit - Ester

## Stored Procedures and Functions
**DUE NOVEMEBR 11TH 11:00 AM**\
Scripts implementing key system operations - Courtney

## Data Scraping Scripts and Documentation
**DUE NOVEMEBR 11TH 11:00 AM**\
Write a python script to scarp data from these 3 websites:

1. [ACM](https://www.acm.org/conferences)
2. [SIGCHI](https://sigchi.org/conferences/)
3. [CIS.IEEE](https://cis.ieee.org/conferences/conference-calendar)
Source code for scraping with error handling and validation.\
Document source websites, sample outputs, and cleaning steps.\
The code for this part must be in Python programming language.\
The results should be saved as a .csv or .json file and being able to import it to MySQL.\
Sam

## Sample Data and Data Cleaning Documentation
**DUE NOVEMEBR 11TH 11:00 AM**\
Create scripts and/or CSV files for sample data inserts, noting how the data was validated and cleaned - Seth

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
