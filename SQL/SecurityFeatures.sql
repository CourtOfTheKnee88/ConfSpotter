-- Security Features Added
-- 1.) Audit Logging
-- 2.) Rate Limiting for Login Attempts
-- 3.) Password Strength Enforcement

USE confspotter;

-- Audit Log Table
CREATE TABLE IF NOT EXISTS AuditLog(
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    username VARCHAR(255) NULL,
    operation_type VARCHAR(50),
    operation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    old_values JSON NULL,
    new_values JSON NULL
);

-- Login Attempts Table for Rate Limiting
CREATE TABLE IF NOT EXISTS LoginAttempts(
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    attempt_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT FALSE
);


-- Password Strength Enforcement Trigger
DELIMITER //
CREATE TRIGGER enforce_password_strength
BEFORE INSERT ON `user`
FOR EACH ROW
BEGIN
    IF LENGTH(NEW.password_hash) < 8 THEN
        SET MESSAGE_TEXT = 'Password must be at least 8 characters long';
    END IF;
END //
DELIMITER ;

