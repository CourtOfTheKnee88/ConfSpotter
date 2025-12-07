CREATE DATABASE IF NOT EXISTS confspotter;
USE confspotter;

-- CORE TABLES
CREATE TABLE Location (
    LID INT AUTO_INCREMENT PRIMARY KEY,
    Street_Address VARCHAR(255) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100) NOT NULL,
    Zip VARCHAR(15) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    -- AKA: "Are location records valid and well-formed?"
    CONSTRAINT check_zip_format CHECK (Zip REGEXP '^[0-9A-Za-z \-]+$'),
    CONSTRAINT check_country_not_empty CHECK (Country <> '')
) ENGINE=InnoDB;

CREATE TABLE Conferences(
    CID INT NOT NULL AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    Start_Date DATETIME NOT NULL,
    End_Date DATETIME NOT NULL,
    Descrip TEXT,
    LID INT NULL,
    link VARCHAR(255) NULL,
    PRIMARY KEY (CID),
    -- AKA: "Does this conference already exist?"
    UNIQUE KEY uq_conference_title (Title),
    -- AKA: "What is the location of this conference?"
    KEY idx_conferences_lid (LID),
    CONSTRAINT fk_conference_location
        FOREIGN KEY (LID) REFERENCES Location(LID)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Papers (
    PID INT NOT NULL AUTO_INCREMENT,
    TypeOfPaper VARCHAR(50) NOT NULL,
    Topic VARCHAR(100) NOT NULL,
    DueDate DATETIME NOT NULL,
    CID INT NULL,
    PRIMARY KEY (PID),
    -- AKA: "Does every paper have a topic?"
    CONSTRAINT chk_topic CHECK (Topic <> ''),
    -- AKA: "Which papers belong to a conference?"
    KEY idx_papers_cid (CID),
    -- AKA: "What deadlines are coming up?"
    KEY idx_due_date (DueDate),
    -- AKA: "Which papers match a topic?"
    KEY idx_topic (Topic),
    CONSTRAINT fk_paper_conference
        FOREIGN KEY (CID) REFERENCES Conferences(CID)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE `user` (
    ID INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255),
    email VARCHAR(255) NULL,
    Phone CHAR(10) NULL,
    Interest_1 VARCHAR(255),
    Interest_2 VARCHAR(255),
    Interest_3 VARCHAR(255),
    PRIMARY KEY (ID),
    -- AKA: "Are phone numbers valid?"
    CONSTRAINT chk_phone CHECK (Phone NOT REGEXP '[^0-9]'),
    -- AKA: "Is this a valid email address?"
    CONSTRAINT email_check CHECK (email IS NULL OR INSTR(email,'@')>0)
) ENGINE=InnoDB;

-- LOCATION-BASED DISCOVERY

-- AKA: "What conferences are in my city/state?"
CREATE INDEX index_city_state ON Location (City, State);

-- AKA: "Find conferences by ZIP code"
CREATE INDEX index_zip ON Location (Zip);

-- AKA: "What conferences are in this country?"
CREATE INDEX index_location_country ON Location (Country);

-- AKA: "Regional browsing (country to state to city)"
CREATE INDEX idx_location_region_full ON Location (Country, State, City);

-- AKA: "Location lookups when joining with conferences"
CREATE INDEX idx_location_city_state_lid ON Location (City, State, LID);

-- CONFERENCE LOOKUP & SEARCH

-- AKA: "Show me conference details with location info"
CREATE INDEX idx_conferences_location ON Conferences (LID);

-- Join conferences with location
SELECT c.CID, c.Title, l.City, l.State, l.Country
FROM Conferences c
JOIN Location l ON c.LID = l.LID;

-- AKA: "Search conferences by title or description"
ALTER TABLE Conferences
ADD FULLTEXT INDEX fullText_conference_title_desc (Title, Descrip);

-- AKA: "What conferences are happening soon or within a date range?"
CREATE INDEX idx_conference_dates_location
ON Conferences (Start_Date, End_Date, LID);

-- AKA: "Show newest/upcoming conferences first"
CREATE INDEX idx_conference_start_desc
ON Conferences (Start_Date DESC);

-- AKA: "Optimize partial title search"
CREATE INDEX idx_conference_title_prefix
ON Conferences (Title(50));

-- AKA: "Search conferences by name and start date"
CREATE INDEX idx_conference_title_start
ON Conferences (Title, Start_Date);

-- AKA: "Find conferences by location and event start time"
CREATE INDEX idx_conferences_lid_start
ON Conferences (LID, Start_Date);

-- AKA: "Join conferences by name and location"
CREATE INDEX idx_conference_title_location
ON Conferences (Title, LID);

-- PAPER DISCOVERY & SUBMISSION 

-- Join papers with conferences
SELECT p.PID, p.Topic, p.DueDate, c.CID, c.Title
FROM Papers p
JOIN Conferences c ON p.CID = c.CID;

-- AKA: "What papers are due for this conference?"
CREATE INDEX idx_papers_cid_duedate_topic
ON Papers (CID, DueDate, Topic);

-- AKA: "Show upcoming submission deadlines"
CREATE INDEX idx_papers_join_cover
ON Papers (CID, Topic, DueDate);

-- AKA: "Which conferences focus on topic X?"
CREATE INDEX idx_conference_topic_title
ON Papers (Topic, CID);

-- USER INTEREST & PROFILE LOOKUPS

-- AKA: "Find a user by email"
CREATE INDEX index_user_email ON user (email);

-- AKA: "Case-insensitive email lookup"
CREATE INDEX idx_user_email_lower ON user ((LOWER(email)));

-- AKA: "Match users by interest areas"
CREATE INDEX index_user_interest1 ON user (Interest_1);
CREATE INDEX index_user_interest2 ON user (Interest_2);
CREATE INDEX index_user_interest3 ON user (Interest_3);

-- AKA: "Multi-interest user matching"
CREATE INDEX idx_user_interests
ON user (Interest_1, Interest_2, Interest_3);

-- JOIN DEMONSTRATIONS (L10 CONCEPTS)

-- AKA: "Show conference and location automatically"
SELECT CID, Title, City, State
FROM Conferences
NATURAL JOIN Location;

-- AKA: "Show all conferences even if no papers exist yet"
SELECT c.Title, p.Topic
FROM Conferences c
LEFT JOIN Papers p ON c.CID = p.CID;

-- AKA: "Show all conferences and papers, even unmatched ones"
SELECT c.Title, p.Topic
FROM Conferences c
LEFT JOIN Papers p ON c.CID = p.CID
UNION
SELECT c.Title, p.Topic
FROM Conferences c
RIGHT JOIN Papers p ON c.CID = p.CID;

-- APPLICATION-DRIVEN ADVANCED QUERIES 

-- AKA: "Which conferences can I submit to after May 2026?"
SELECT DISTINCT c.CID, c.Title, p.DueDate
FROM Conferences c
JOIN Papers p ON c.CID = p.CID
WHERE p.DueDate > '2026-05-01'
ORDER BY p.DueDate;

CREATE INDEX idx_papers_deadline_conference
ON Papers (DueDate, CID);

-- AKA: "What type of papers can be submitted to conference X this year?"
SELECT DISTINCT p.TypeOfPaper
FROM Papers p
JOIN Conferences c ON p.CID = c.CID
WHERE c.Title = 'Conference X'
  AND YEAR(p.DueDate) = YEAR(CURDATE());

CREATE INDEX idx_papers_conference_type_date
ON Papers (CID, TypeOfPaper, DueDate);

-- AKA: "What conferences are happening in my country this year?"
SELECT c.Title, c.Start_Date, l.Country
FROM Conferences c
JOIN Location l ON c.LID = l.LID
WHERE l.Country = 'USA'
  AND YEAR(c.Start_Date) = YEAR(CURDATE());

CREATE INDEX idx_conference_geography_year
ON Conferences (LID, Start_Date);