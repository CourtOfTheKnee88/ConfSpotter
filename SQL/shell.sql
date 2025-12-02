CREATE DATABASE IF NOT EXISTS confspotter;
USE confspotter;

CREATE TABLE Location (
    LID INT AUTO_INCREMENT PRIMARY KEY,
    Street_Address VARCHAR(255) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100) NOT NULL,
    Zip VARCHAR(15) NOT NULL,
    Country VARCHAR(100) NOT NULL,
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
    UNIQUE KEY uq_conference_title (Title),
    KEY idx_conferences_lid (LID),
    CONSTRAINT fk_conference_location FOREIGN KEY (LID) REFERENCES Location(LID) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE Papers (
    PID INT NOT NULL AUTO_INCREMENT,
    TypeOfPaper VARCHAR(50) NOT NULL,
    Topic VARCHAR(100) NOT NULL,
    DueDate DATETIME NOT NULL,
    CID INT NULL,
    PRIMARY KEY (PID),
    CONSTRAINT chk_topic CHECK (Topic <> ''),
    KEY idx_papers_cid (CID),
    KEY idx_due_date (DueDate),
    KEY idx_topic (Topic),
    CONSTRAINT fk_paper_conference FOREIGN KEY (CID) REFERENCES Conferences(CID) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE `user` (
    ID INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL, 
    email VARCHAR(255) NULL,
    Phone CHAR(10) NULL,
    Interest_1 VARCHAR(255),
    Interest_2 VARCHAR(255),
    Interest_3 VARCHAR(255),
    PRIMARY KEY (ID),
    CONSTRAINT chk_phone CHECK (Phone NOT REGEXP '[^0-9]'),
    CONSTRAINT email_check CHECK (email IS NULL OR INSTR(email,'@')>0)
) ENGINE=InnoDB;

CREATE INDEX index_city_state ON Location (City, State);
CREATE INDEX index_zip ON Location (Zip);

-- Index for join between Conferences and Location (conferences.LID)
CREATE INDEX idx_conferences_location ON Conferences (LID);

-- Join Conferences with Location
SELECT c.CID, c.Title, l.City, l.State, l.Country
FROM Conferences c
JOIN Location l ON c.LID = l.LID;

-- Join Papers with Conferences
SELECT p.PID, p.Topic, p.DueDate, c.CID, c.Title
FROM Papers p
JOIN Conferences c ON p.CID = c.CID;

-- Index to speed up lookups when searching by email
CREATE INDEX index_user_email ON user(email);

-- Index to filter user by interests
CREATE INDEX index_user_interest1 ON user(Interest_1);
CREATE INDEX index_user_interest2 ON user(Interest_2);
CREATE INDEX index_user_interest3 ON user(Interest_3);

-- Index to filter by geographic region (country)
CREATE INDEX index_location_country ON Location(Country);

-- Index to improve text searches for conferences by title or keywords
-- How full text works: https://dev.mysql.com/doc/refman/8.4/en/innodb-fulltext-index.html
ALTER TABLE Conferences
ADD FULLTEXT INDEX fullText_conference_title_desc (Title, Descrip);

-- New INDEXES (Added in PHASE III):

-- Index for upcoming papers by conference
CREATE INDEX idx_papers_cid_duedate_topic
ON Papers (CID, DueDate, Topic);

-- Index for location-based filtering
CREATE INDEX idx_location_city_state_lid
ON Location (City, State, LID);

-- Index for conference timeline
CREATE INDEX idx_conference_dates_location
ON Conferences (Start_Date, End_Date, LID);

-- Index for descending order, e.g., newest first
CREATE INDEX idx_conference_start_desc
ON Conferences (Start_Date DESC);

-- Index for large text columns
CREATE INDEX idx_conference_title_prefix
ON Conferences (Title(50));

-- Index for papers + conferences join
CREATE INDEX idx_papers_join_cover
ON Papers (CID, Topic, DueDate);

-- Index for multi-user interests
CREATE INDEX idx_user_interests
ON user (Interest_1, Interest_2, Interest_3);

-- Index for lower-cased email, case sensitive
CREATE INDEX idx_user_email_lower
ON user ((LOWER(email)));

-- Index for regional conferences
CREATE INDEX idx_location_region_full
ON Location (Country, State, City);

-- Index for multi-column conferences search, title and start date
CREATE INDEX idx_conference_title_start
ON Conferences (Title, Start_Date);

-- Index for location for conference lookups (a kind of reverse lookup)
CREATE INDEX idx_conferences_lid_start
ON Conferences (LID, Start_Date);

-- Index for joining user and conferences via interests
CREATE INDEX idx_conference_topic_title
ON Papers (Topic, CID);

-- Index for multi-table join for conferences title and location
CREATE INDEX idx_conference_title_location
ON Conferences (Title, LID);
