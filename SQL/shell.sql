CREATE DATABASE confspotter;
use confspotter;

Create table Papers (
    PaperID INT PRIMARY KEY,
    TypeOfPaper VARCHAR(50),
    Topic VARCHAR(100),
    DueDate DATETIME
)

CREATE TABLE user (
	Interest_1 varchar(255),
    Interest_2 varchar(255),
    Interest_3 varchar(255),
    Phone char(10) CONSTRAINT chk_phone CHECK (phone not like '%[^0-9]%'),
    username varchar(255),
    email varchar(255) constraint email_check CHECK(instr(email,'%@%.%')>0),
    ID varchar(255),
    PRIMARY KEY (ID)
)

create table Conferences(
    CID varchar(6) not null auto_increment, 
    Title varchar(99) not null,
    State_Date DATETIME not null,
    End_Date DATETIME not null,
    Descrip varchar(99) not null,
    primary key (CID),
    unique (CID),
    unique (Title)
);

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