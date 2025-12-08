-- FILE: sample_project_data.sql 
-- Description: Stores small sample of the Conferences database
-- Author: esthergreene
-- Project: Conference Spotter - Phase II
-- Code created by author, example data ideas created by ChatGPT.

USE confspotter;


-- Location Table 
INSERT INTO Location (Street_Address, City, State, Zip, Country) VALUES
('40 Free St', 'Portland', 'ME', '04101', 'USA'),
('1 Civic Center Dr', 'Augusta', 'ME', '04330', 'USA'),
('300 Main St', 'Bangor', 'ME', '04401', 'USA'),
('141 Main St', 'Bar Harbor', 'ME', '04609', 'USA');


-- Conferences Table 
INSERT INTO Conferences (Title, Start_Date, End_Date, Descrip, LID, Link) VALUES
('Maine AI Summit 2026', '2026-03-10 09:00:00', '2026-03-12 17:00:00', 'Leading conference for artificial intelligence research.', 1, 'https://maineaisummit2026.com'),
('Sustainable Energy Expo ME', '2026-06-05 08:30:00', '2026-06-07 18:00:00', 'Focus on renewable technologies and policy.', 2, 'https://sustainableenergyme.org'),
('New England Digital Marketing Conference', '2026-11-20 10:00:00', '2026-11-20 19:30:00', 'Annual event covering SEO, content, and social media.', 3, 'https://digitalmarketingconf.com');


-- Papers Table 
INSERT INTO Papers (PID, TypeOfPaper, Topic, DueDate, CID) VALUES
(1, 'Full Paper', 'Explainable AI in Healthcare', '2025-12-01 23:59:00', 1),
(2, 'Short Paper', 'Geothermal Power Efficiency', '2026-01-15 23:59:00', 2),
(3, 'Poster', 'Optimizing Ad Campaigns with ML', '2026-09-01 23:59:00', 3),
(4, 'Full Paper', 'Ethics in Large Language Models', '2025-12-01 23:59:00', 2),
(5, 'Abstract Paper', 'AI and The Effect On The Brain', '2025-12-10 23:59:00', 1);


-- User Table 
INSERT INTO user (ID, username, password_hash, email, Phone, Interest_1, Interest_2, Interest_3) VALUES
(1, 'ajohnson', 'P@ssw0rd!', 'a.johnson@corp.com', '5551234567', 'AI', 'Ethics', 'Data Science'),
(2, 'mgarcia', 'P@ssw0rd!', 'maria.g@webmail.org', '5559876543', 'Renewables', 'Policy', 'Solar'),
(3, 'clee', 'P@ssw0rd!', 'c.lee@university.edu', '5551112222', 'Marketing', 'ML', 'Analytics');