-- ============================================================
-- SQL Stored Procedures
-- ============================================================

USE alumni_management;

DROP PROCEDURE IF EXISTS GetAlumniByFilter;

DELIMITER $$

CREATE PROCEDURE GetAlumniByFilter(
    IN p_department_id   INT,       -- NULL to ignore department filter
    IN p_graduation_year YEAR       -- NULL to ignore year filter
)
BEGIN
    SELECT
        a.alumni_id,
        u.full_name,
        u.email,
        d.department_name,
        a.graduation_year,
        a.current_company,
        a.job_title,
        a.skills
    FROM Alumni a
    INNER JOIN Users      u ON a.user_id       = u.user_id
    INNER JOIN Department d ON a.department_id = d.department_id
    WHERE u.account_status = 'approved'
      AND (p_department_id   IS NULL OR a.department_id   = p_department_id)
      AND (p_graduation_year IS NULL OR a.graduation_year = p_graduation_year)
    ORDER BY a.graduation_year DESC, u.full_name ASC;
END$$

DELIMITER ;
