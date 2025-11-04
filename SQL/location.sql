-- Table: Location
-- Description: Stores conference Location details
-- Author: esthergreene
-- Project: Conference Spotter - Phase II

/*
Citations:
https://www.w3schools.com/mysql/mysql_create_table.asp
https://dev.mysql.com/doc/refman/8.4/en/example-auto-increment.html
https://www.w3schools.com/mysql/mysql_constraints.asp
https://www.w3schools.com/mysql/mysql_check.asp
https://www.geeksforgeeks.org/mysql/mysql-regular-expressions-regexp/
https://dev.mysql.com/doc/refman/8.4/en/innodb-introduction.html
*/
CREATE TABLE Location (
	LID INT AUTO_INCREMENT PRIMARY KEY,
    Street_Address VARCHAR(255) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100) NOT NULL,
    Zip VARCHAR(15) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    
    CONSTRAINT check_zip_format CHECK (Zip REGEXP '^[9Aza-z-=]+$'),
    CONSTRAINT check_country_not_empty CHECK (Country <> '')
) ENGINE=InnoDB;

CREATE INDEX index_city_state ON Location (City, State);
CREATE INDEX index_zip ON Location (Zip);

    /*
    We'll need to add something like this to the Conferences Table:
    ALTER TABLE Conferences
    ADD COLUMN LID INT NOT NULL,
    ADD CONSTRAINT fk_conference_location
		FOREIGN KEY (LID)
        REFERENCES Location(LID)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
    */
    
    /*
    Example data to insert:
    INSERT INTO Location (Street_Address, City, State, Zip, Country)
    VALUES
    ('123 Oak St', 'Portland', 'Maine', '04101', 'USA'),
    ('456 Oak Ave', 'Bangor', 'Maine', '04401', 'USA'),
    ('789 Pine Blvd', 'Augusta', 'Maine', '04330', 'USA');
    */

