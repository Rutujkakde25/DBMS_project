-- ============================================================
-- SQL Views Definition
-- ============================================================

USE alumni_management;

-- View 1: alumni_directory_view
-- Exposes public alumni profile details with department name
CREATE OR REPLACE VIEW alumni_directory_view AS
SELECT
    a.alumni_id,
    u.full_name,
    u.email,
    d.department_name,
    a.graduation_year,
    a.current_company,
    a.job_title,
    a.skills,
    a.linkedin_url,
    a.bio,
    u.account_status
FROM Alumni a
INNER JOIN Users      u ON a.user_id       = u.user_id
INNER JOIN Department d ON a.department_id = d.department_id
WHERE u.account_status = 'approved';

-- View 2: job_opportunities_view
-- Aggregates job postings along with posting alumni's information
CREATE OR REPLACE VIEW job_opportunities_view AS
SELECT
    j.job_id,
    j.company_name,
    j.job_title,
    j.job_description,
    j.job_type,
    j.application_link,
    j.location,
    j.deadline,
    j.created_at,
    u.full_name       AS posted_by,
    d.department_name AS alumni_department
FROM Job j
INNER JOIN Alumni     a ON j.alumni_id     = a.alumni_id
INNER JOIN Users      u ON a.user_id       = u.user_id
INNER JOIN Department d ON a.department_id = d.department_id
WHERE u.account_status = 'approved';
