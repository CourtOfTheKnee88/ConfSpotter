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

Team Leader - Courtney Jackson (Courtney.Jackson@maine.edu)
Esther Greene (esther.greene@maine.edu), Samuel Fickett (Samuel.Fickett@maine.edu), Seth Tedder (Seth.Tedder@maine.edu)
Google Drive: https://docs.google.com/document/d/17Stc62MJ4LH-gEOT_NdcwDbSWMRVzchYqExX04Cgea0/edit?usp=sharing

# PHASE II:
Location Table:
The Location table stores physical address information for each conference. It includes validation constraints, primary key (LID),
and indexing for efficient lookups by city/state and zip. The table is linked to Conferences via a foreign key relationship (LID).
