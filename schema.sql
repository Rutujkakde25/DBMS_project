-- ============================================================
-- Alumni Management System - Database Schema
-- Database: alumni_management
-- ============================================================

-- Create and use the database
CREATE DATABASE IF NOT EXISTS alumni_management
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE alumni_management;

-- ============================================================
-- TABLE 1: Department
-- Stores university departments (1NF, 2NF, 3NF compliant)
-- ============================================================
CREATE TABLE IF NOT EXISTS Department (
    department_id   INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);

-- ============================================================
-- TABLE 2: Users
-- Central authentication table for all roles
-- ============================================================
CREATE TABLE IF NOT EXISTS Users (
    user_id        INT AUTO_INCREMENT PRIMARY KEY,
    full_name      VARCHAR(150) NOT NULL,
    email          VARCHAR(150) NOT NULL UNIQUE,
    password_hash  VARCHAR(256) NOT NULL,
    role           ENUM('admin', 'alumni', 'student') NOT NULL,
    account_status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Index on email for fast login lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON Users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON Users(role);

-- ============================================================
-- TABLE 3: Alumni
-- Extended profile for alumni users
-- ============================================================
CREATE TABLE IF NOT EXISTS Alumni (
    alumni_id       INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL UNIQUE,
    department_id   INT NOT NULL,
    graduation_year YEAR NOT NULL,
    current_company VARCHAR(150),
    job_title       VARCHAR(150),
    skills          TEXT,
    linkedin_url    VARCHAR(300),
    bio             TEXT,
    CONSTRAINT fk_alumni_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_alumni_dept FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

-- Indexes for commonly searched columns
CREATE INDEX IF NOT EXISTS idx_alumni_dept ON Alumni(department_id);
CREATE INDEX IF NOT EXISTS idx_alumni_year ON Alumni(graduation_year);
CREATE INDEX IF NOT EXISTS idx_alumni_company ON Alumni(current_company);

-- ============================================================
-- TABLE 4: Student
-- Extended profile for student users
-- ============================================================
CREATE TABLE IF NOT EXISTS Student (
    student_id    INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT NOT NULL UNIQUE,
    department_id INT NOT NULL,
    current_year  INT NOT NULL CHECK (current_year BETWEEN 1 AND 5),
    skills        TEXT,
    interests     TEXT,
    CONSTRAINT fk_student_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_student_dept FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

CREATE INDEX IF NOT EXISTS idx_student_dept ON Student(department_id);

-- ============================================================
-- TABLE 5: Job
-- Job and internship postings by alumni
-- ============================================================
CREATE TABLE IF NOT EXISTS Job (
    job_id           INT AUTO_INCREMENT PRIMARY KEY,
    alumni_id        INT NOT NULL,
    company_name     VARCHAR(150) NOT NULL,
    job_title        VARCHAR(150) NOT NULL,
    job_description  TEXT NOT NULL,
    job_type         ENUM('Internship', 'Full-time') NOT NULL,
    application_link VARCHAR(300),
    location         VARCHAR(150),
    deadline         DATE,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_job_alumni FOREIGN KEY (alumni_id) REFERENCES Alumni(alumni_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_job_alumni ON Job(alumni_id);
CREATE INDEX IF NOT EXISTS idx_job_type ON Job(job_type);

-- ============================================================
-- TABLE 6: Mentorship
-- Mentorship requests from students to alumni
-- ============================================================
CREATE TABLE IF NOT EXISTS Mentorship (
    mentorship_id  INT AUTO_INCREMENT PRIMARY KEY,
    student_id     INT NOT NULL,
    alumni_id      INT NOT NULL,
    message        TEXT,
    request_status ENUM('Pending', 'Accepted', 'Rejected') NOT NULL DEFAULT 'Pending',
    requested_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mentorship_student FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_mentorship_alumni  FOREIGN KEY (alumni_id)  REFERENCES Alumni(alumni_id) ON DELETE CASCADE,
    -- One student can only send one request to a specific alumni
    UNIQUE KEY uq_mentorship (student_id, alumni_id)
);

CREATE INDEX IF NOT EXISTS idx_mentorship_student ON Mentorship(student_id);
CREATE INDEX IF NOT EXISTS idx_mentorship_alumni ON Mentorship(alumni_id);

-- ============================================================
-- TABLE 7: Event
-- University events (alumni meets, webinars, etc.)
-- ============================================================
CREATE TABLE IF NOT EXISTS Event (
    event_id    INT AUTO_INCREMENT PRIMARY KEY,
    event_name  VARCHAR(200) NOT NULL,
    description TEXT,
    event_date  DATE NOT NULL,
    venue       VARCHAR(200),
    created_by  INT NOT NULL,
    CONSTRAINT fk_event_creator FOREIGN KEY (created_by) REFERENCES Users(user_id)
);

-- ============================================================
-- TABLE 8: Event_Registration
-- Junction table: many users can register for many events
-- ============================================================
CREATE TABLE IF NOT EXISTS Event_Registration (
    registration_id   INT AUTO_INCREMENT PRIMARY KEY,
    event_id          INT NOT NULL,
    user_id           INT NOT NULL,
    registration_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    attendance_status ENUM('Registered', 'Attended', 'Absent') NOT NULL DEFAULT 'Registered',
    CONSTRAINT fk_reg_event FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE,
    CONSTRAINT fk_reg_user  FOREIGN KEY (user_id)  REFERENCES Users(user_id) ON DELETE CASCADE,
    -- Prevent duplicate registrations (UNIQUE constraint)
    UNIQUE KEY uq_event_user (event_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_reg_event ON Event_Registration(event_id);
CREATE INDEX IF NOT EXISTS idx_reg_user  ON Event_Registration(user_id);

-- ============================================================
-- VIEWS
-- ============================================================

-- View 1: alumni_directory_view
-- Shows public alumni information with department name
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
-- Shows all job postings with alumni and department info
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
    u.full_name   AS posted_by,
    d.department_name AS alumni_department
FROM Job j
INNER JOIN Alumni     a ON j.alumni_id     = a.alumni_id
INNER JOIN Users      u ON a.user_id       = u.user_id
INNER JOIN Department d ON a.department_id = d.department_id
WHERE u.account_status = 'approved';

-- ============================================================
-- STORED PROCEDURE
-- Get alumni filtered by department or graduation year
-- ============================================================
DROP PROCEDURE IF EXISTS GetAlumniByFilter;

DELIMITER $$

CREATE PROCEDURE GetAlumniByFilter(
    IN p_department_id   INT,       -- NULL to skip department filter
    IN p_graduation_year YEAR       -- NULL to skip year filter
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

-- ============================================================
-- TRIGGER
-- Prevent duplicate or invalid mentorship requests:
-- Ensures the alumni's user account is approved before
-- a student can send a mentorship request.
-- (Foreign keys handle referential integrity; this trigger
--  enforces the business rule about account status.)
-- ============================================================
DROP TRIGGER IF EXISTS trg_validate_mentorship;

DELIMITER $$

CREATE TRIGGER trg_validate_mentorship
BEFORE INSERT ON Mentorship
FOR EACH ROW
BEGIN
    DECLARE alumni_status VARCHAR(20);

    -- Check if the alumni's account is approved
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
