USE confspotter;

-- Procedure to check if a conference name already exists in the database
DELIMITER //
DROP PROCEDURE IF EXISTS CheckConferenceExists //
CREATE PROCEDURE CheckConferenceExists(
    IN conference_title VARCHAR(255),
    OUT conferenceExists BOOLEAN
)
BEGIN
    DECLARE conference_count INT DEFAULT 0;
    SELECT COUNT(*) INTO conference_count
    FROM Conferences
    WHERE Title = conference_title;
    IF conference_count > 0 THEN
        SET conferenceExists = TRUE;
    ELSE
        SET conferenceExists = FALSE;
    END IF;
END //
DELIMITER ;

-- Procedure to check if a user with given email or phone number already exists
DELIMITER //
DROP PROCEDURE IF EXISTS CheckUserExists //
CREATE PROCEDURE CheckUserExists(
    IN user_email VARCHAR(255),
    IN user_phone CHAR(10),
    OUT exists_flag BOOLEAN,
    OUT existing_user_id INT
)
BEGIN
    DECLARE user_count INT DEFAULT 0;
    DECLARE found_user_id INT DEFAULT NULL;
    
    SELECT COUNT(*), MAX(ID) INTO user_count, found_user_id
    FROM user
    WHERE (email = user_email AND user_email IS NOT NULL)
       OR (Phone = user_phone AND user_phone IS NOT NULL);
    
    IF user_count > 0 THEN
        SET exists_flag = TRUE;
        SET existing_user_id = found_user_id;
    ELSE
        SET exists_flag = FALSE;
        SET existing_user_id = NULL;
    END IF;
END //
DELIMITER ;

-- Triggers

-- Trigger to automatically delete conferences after their end date has passed
-- Runs daily via an event scheduler
DELIMITER //
CREATE EVENT IF NOT EXISTS DeleteExpiredConferences
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    -- Delete conferences where end date is in the past
    DELETE FROM Conferences
    WHERE End_Date < NOW();
END //
DELIMITER ;

-- Stored procedure to manually clean up expired conferences
DELIMITER //
DROP PROCEDURE IF EXISTS CleanupExpiredConferences //
CREATE PROCEDURE CleanupExpiredConferences()
BEGIN
    DECLARE deleted_count INT DEFAULT 0;
    DELETE FROM Conferences
    WHERE End_Date < NOW();
    SELECT ROW_COUNT() AS conferences_deleted;
END //
DELIMITER ;
DELIMITER ;
