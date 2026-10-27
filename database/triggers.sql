-- ============================================================
-- SQL Triggers
-- ============================================================

USE alumni_management;

DROP TRIGGER IF EXISTS trg_validate_mentorship;

DELIMITER $$

CREATE TRIGGER trg_validate_mentorship
BEFORE INSERT ON Mentorship
FOR EACH ROW
BEGIN
    DECLARE alumni_status VARCHAR(20);

    -- Enforce that mentorship requests are only sent to approved alumni accounts
    SELECT u.account_status INTO alumni_status
    FROM Alumni al
    INNER JOIN Users u ON al.user_id = u.user_id
    WHERE al.alumni_id = NEW.alumni_id;

    IF alumni_status IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid alumni ID: alumni does not exist.';
    ELSEIF alumni_status != 'approved' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot send mentorship request: alumni account is not approved.';
    END IF;
END$$

DELIMITER ;
