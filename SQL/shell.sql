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
