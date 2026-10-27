# ============================================================
# Alumni Networking Management System - SQL Queries Reference
# For College DBMS Evaluation & Viva Demonstrations
# ============================================================

USE alumni_management;

-- ============================================================
-- 1. BASIC DDL & DML OPERATIONS
-- ============================================================

-- INSERT example (Adding a new department)
INSERT INTO Department (department_name) VALUES ('Data Science & AI');

-- SELECT example
SELECT * FROM Users WHERE role = 'alumni' AND account_status = 'approved';

-- UPDATE example
UPDATE Alumni 
SET current_company = 'Google LLC', job_title = 'Staff Software Engineer' 
WHERE alumni_id = 1;

-- DELETE example (with CASCADE effect)
-- DELETE FROM Users WHERE user_id = 11;


-- ============================================================
-- 2. JOINS DEMONSTRATIONS
-- ============================================================

-- A. INNER JOIN: Fetch approved alumni with department details
SELECT 
    u.full_name,
    u.email,
    d.department_name,
    a.graduation_year,
    a.current_company,
    a.job_title
FROM Alumni a
INNER JOIN Users u ON a.user_id = u.user_id
INNER JOIN Department d ON a.department_id = d.department_id
WHERE u.account_status = 'approved';

-- B. LEFT JOIN: Find students who have NOT sent any mentorship requests
SELECT 
    u.full_name,
    u.email,
    d.department_name,
    s.current_year
FROM Student s
JOIN Users u ON s.user_id = u.user_id
JOIN Department d ON s.department_id = d.department_id
LEFT JOIN Mentorship m ON s.student_id = m.student_id
WHERE m.mentorship_id IS NULL;

-- C. MULTIPLE JOINS: Alumni, their current companies, and posted job openings
SELECT 
    u.full_name AS alumni_name,
    d.department_name,
    j.company_name,
    j.job_title,
    j.job_type,
    j.location,
    j.deadline
FROM Job j
INNER JOIN Alumni a ON j.alumni_id = a.alumni_id
INNER JOIN Users u ON a.user_id = u.user_id
INNER JOIN Department d ON a.department_id = d.department_id
ORDER BY j.created_at DESC;


-- ============================================================
-- 3. AGGREGATE FUNCTIONS & GROUP BY
-- ============================================================

-- Count of alumni per department
SELECT 
    d.department_name, 
    COUNT(a.alumni_id) AS total_alumni
FROM Department d
LEFT JOIN Alumni a ON d.department_id = a.department_id
LEFT JOIN Users u ON a.user_id = u.user_id AND u.account_status = 'approved'
GROUP BY d.department_id, d.department_name
ORDER BY total_alumni DESC;

-- Count of alumni by graduation year
SELECT 
    a.graduation_year, 
    COUNT(*) AS total_graduates
FROM Alumni a
JOIN Users u ON a.user_id = u.user_id
WHERE u.account_status = 'approved'
GROUP BY a.graduation_year
ORDER BY a.graduation_year DESC;

-- Number of job postings per company
SELECT 
    company_name, 
    COUNT(*) AS total_postings
FROM Job
GROUP BY company_name
ORDER BY total_postings DESC;

-- Mentorship requests grouped by status
SELECT 
    request_status, 
    COUNT(*) AS total_requests
FROM Mentorship
GROUP BY request_status;

-- Total registrations per event
SELECT 
    e.event_id,
    e.event_name,
    COUNT(er.registration_id) AS total_registrations
FROM Event e
LEFT JOIN Event_Registration er ON e.event_id = er.event_id
GROUP BY e.event_id, e.event_name;


-- ============================================================
-- 4. SUBQUERY WITH HAVING
-- Find departments with more alumni than the average alumni per department
-- ============================================================
SELECT 
    d.department_name, 
    COUNT(a.alumni_id) AS alumni_count
FROM Department d
JOIN Alumni a ON d.department_id = a.department_id
JOIN Users u ON a.user_id = u.user_id AND u.account_status = 'approved'
GROUP BY d.department_id, d.department_name
HAVING alumni_count > (
    SELECT AVG(dept_count) FROM (
        SELECT COUNT(a2.alumni_id) AS dept_count
        FROM Department d2
        LEFT JOIN Alumni a2 ON d2.department_id = a2.department_id
        GROUP BY d2.department_id
    ) AS sub
);
