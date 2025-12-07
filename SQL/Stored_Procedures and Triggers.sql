USE confspotter;

-- Procedure to check if a conference name already exists in the database
DELIMITER //
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

-- Function to check if a user with given email or phone number already exists
-- Returns 1 if exists, 0 if not (compatible with triggers)
DELIMITER //
<<<<<<< Updated upstream
CREATE PROCEDURE CheckUserExists(
    IN user_email VARCHAR(255),
    IN user_phone CHAR(10),
    OUT exists_flag BOOLEAN,
    OUT existing_user_id INT
)
=======
DROP PROCEDURE IF EXISTS CheckUserExists //
DROP FUNCTION IF EXISTS CheckUserExists //
CREATE FUNCTION CheckUserExists(
    user_email VARCHAR(255),
    user_phone CHAR(10),
    user_name VARCHAR(255)
) RETURNS BOOLEAN
DETERMINISTIC
READS SQL DATA
>>>>>>> Stashed changes
BEGIN
    DECLARE user_count INT DEFAULT 0;
    
    SELECT COUNT(*) INTO user_count
    FROM user
    WHERE (email = user_email AND user_email IS NOT NULL)
       OR (Phone = user_phone AND user_phone IS NOT NULL);
    
    RETURN user_count > 0;
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
CREATE PROCEDURE CleanupExpiredConferences()
BEGIN
    DECLARE deleted_count INT DEFAULT 0;
    DELETE FROM Conferences
    WHERE End_Date < NOW();
    SELECT ROW_COUNT() AS conferences_deleted;
END //
DELIMITER ;
