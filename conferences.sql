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