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