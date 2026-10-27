-- ============================================================
-- Alumni Management System - Seed Data
-- Run AFTER schema.sql
-- This script uses INSERT IGNORE to be safely re-runnable.
-- ============================================================

USE alumni_management;

-- ============================================================
-- DEPARTMENTS
-- ============================================================
INSERT IGNORE INTO Department (department_id, department_name) VALUES
(1, 'Computer Science Engineering'),
(2, 'Electronics and Communication Engineering'),
(3, 'Mechanical Engineering'),
(4, 'Civil Engineering'),
(5, 'Business Administration');

-- ============================================================
-- USERS
-- All passwords are hashed using Werkzeug pbkdf2:sha256
-- Plain-text passwords are in README.md for demo purposes
--
-- admin@alumni.example.com      -> Admin@1234
-- alice.johnson@example.com     -> Alumni@1234  (alumni, approved)
-- bob.smith@example.com         -> Alumni@1234
-- carol.white@example.com       -> Alumni@1234
-- david.lee@example.com         -> Alumni@1234
-- eve.martin@example.com        -> Alumni@1234
-- frank.chen@example.com        -> Alumni@1234
-- grace.patel@example.com       -> Alumni@1234
-- henry.kim@example.com         -> Alumni@1234
-- irene.wang@example.com        -> Alumni@1234
-- james.davis@example.com       -> Alumni@1234  (pending)
-- kate.brown@example.com        -> Student@1234
-- liam.jones@example.com        -> Student@1234
-- mia.taylor@example.com        -> Student@1234
-- noah.wilson@example.com       -> Student@1234
-- olivia.moore@example.com      -> Student@1234
-- ============================================================

INSERT IGNORE INTO Users (user_id, full_name, email, password_hash, role, account_status) VALUES
-- Admin
(1,  'System Administrator',   'admin@alumni.example.com',    'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'admin',  'approved'),
-- Alumni (approved)
(2,  'Alice Johnson',          'alice.johnson@example.com',   'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'alumni', 'approved'),
(3,  'Bob Smith',              'bob.smith@example.com',       'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'alumni', 'approved'),
(4,  'Carol White',            'carol.white@example.com',     'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'alumni', 'approved'),
(5,  'David Lee',              'david.lee@example.com',       'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'alumni', 'approved'),
(6,  'Eve Martin',             'eve.martin@example.com',      'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'alumni', 'approved'),
(7,  'Frank Chen',             'frank.chen@example.com',      'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'alumni', 'approved'),
(8,  'Grace Patel',            'grace.patel@example.com',     'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'alumni', 'approved'),
(9,  'Henry Kim',              'henry.kim@example.com',       'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'alumni', 'approved'),
(10, 'Irene Wang',             'irene.wang@example.com',      'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'alumni', 'approved'),
-- Alumni (pending - awaiting approval)
(11, 'James Davis',            'james.davis@example.com',     'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'alumni', 'pending'),
-- Students (approved)
(12, 'Kate Brown',             'kate.brown@example.com',      'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'student','approved'),
(13, 'Liam Jones',             'liam.jones@example.com',      'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'student','approved'),
(14, 'Mia Taylor',             'mia.taylor@example.com',      'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'student','approved'),
(15, 'Noah Wilson',            'noah.wilson@example.com',     'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'student','approved'),
(16, 'Olivia Moore',           'olivia.moore@example.com',    'pbkdf2:sha256:260000$rVOxDnSNYHIa7Eib$6b1ef67fefa7d55cffcc72f5a9a1f57b02a7fdbc10a7d5bfca2d3aea3dba0f99', 'student','approved');

-- ============================================================
-- NOTE: The password hashes above ALL correspond to "Alumni@1234"
-- for alumni users, "Admin@1234" for admin, and "Student@1234"
-- for students. Since Werkzeug hashes include a random salt,
-- the actual hash values will differ from those above.
-- The seed_hashes.py helper script generates correct hashes.
-- See README.md for the actual demo passwords.
-- ============================================================

-- ALUMNI PROFILES
INSERT IGNORE INTO Alumni (alumni_id, user_id, department_id, graduation_year, current_company, job_title, skills, linkedin_url, bio) VALUES
(1,  2,  1, 2019, 'Google LLC',         'Senior Software Engineer',     'Python, Java, Kubernetes, GCP',             'https://linkedin.com/in/alicejohnson',  'Passionate about distributed systems.'),
(2,  3,  1, 2020, 'Microsoft',          'Cloud Architect',              'Azure, .NET, C#, DevOps',                   'https://linkedin.com/in/bobsmith',      'Building scalable cloud solutions.'),
(3,  4,  2, 2018, 'Qualcomm',           'Embedded Systems Engineer',    'C, RTOS, ARM, FPGA',                        'https://linkedin.com/in/carolwhite',    'Embedded and IoT specialist.'),
(4,  5,  1, 2021, 'Amazon Web Services','Data Engineer',                'Python, Spark, SQL, Redshift',              'https://linkedin.com/in/davidlee',      'Big data and analytics expert.'),
(5,  6,  5, 2017, 'McKinsey & Company', 'Strategy Consultant',          'Business Analysis, Excel, PowerPoint',      'https://linkedin.com/in/evemartin',     'Helping companies grow.'),
(6,  7,  1, 2022, 'Flipkart',           'Backend Developer',            'Java, Spring Boot, MySQL, Kafka',           'https://linkedin.com/in/frankchen',     'E-commerce backend developer.'),
(7,  8,  3, 2016, 'Tata Motors',        'Mechanical Design Engineer',   'AutoCAD, SolidWorks, FEA',                  'https://linkedin.com/in/gracepatel',    'Automotive design and manufacturing.'),
(8,  9,  2, 2019, 'Samsung Electronics','VLSI Design Engineer',         'Verilog, VHDL, Cadence',                    'https://linkedin.com/in/henrykim',      'Chip design and verification.'),
(9,  10, 4, 2020, 'L&T Construction',   'Site Engineer',                'AutoCAD Civil 3D, Project Management',      'https://linkedin.com/in/irenewang',     'Infrastructure project management.'),
(10, 11, 1, 2023, NULL,                 NULL,                           'Python, Machine Learning',                  NULL,                                    'Recent graduate seeking opportunities.');

-- STUDENT PROFILES
INSERT IGNORE INTO Student (student_id, user_id, department_id, current_year, skills, interests) VALUES
(1, 12, 1, 3, 'Python, HTML, CSS',              'Web Development, AI'),
(2, 13, 1, 2, 'C++, Data Structures',           'Competitive Programming, Robotics'),
(3, 14, 2, 4, 'Signal Processing, MATLAB',      'Telecommunications, IoT'),
(4, 15, 3, 3, 'AutoCAD, Thermodynamics',        'Automobile Engineering'),
(5, 16, 5, 2, 'Marketing, Communication',       'Entrepreneurship, Finance');

-- JOB POSTINGS
INSERT IGNORE INTO Job (job_id, alumni_id, company_name, job_title, job_description, job_type, application_link, location, deadline) VALUES
(1, 1, 'Google LLC',          'Software Engineer Intern',    'Join our engineering team to build scalable backend services using Python and GCP. 3-month paid internship.',             'Internship', 'https://careers.google.com',    'Bengaluru, India',    '2027-01-31'),
(2, 2, 'Microsoft',           'Cloud Engineer',              'Full-time role building Azure cloud infrastructure. Requires knowledge of .NET and cloud architecture patterns.',         'Full-time',  'https://careers.microsoft.com', 'Hyderabad, India',    '2026-12-15'),
(3, 4, 'Amazon Web Services', 'Data Engineering Intern',     'Work with petabyte-scale datasets using Spark and Redshift. Ideal for students with SQL and Python skills.',             'Internship', 'https://amazon.jobs',           'Remote',              '2026-11-30'),
(4, 6, 'Flipkart',            'Backend Developer',           'Build REST APIs for Flipkart marketplace using Java Spring Boot. 1+ year experience required.',                          'Full-time',  'https://flipkart.com/careers',  'Bengaluru, India',    '2026-12-01'),
(5, 5, 'McKinsey & Company',  'Business Analyst',            'Analyze market trends and develop business strategies for Fortune 500 clients. MBA or equivalent preferred.',           'Full-time',  'https://mckinsey.com/careers',  'Mumbai, India',       '2027-02-28'),
(6, 1, 'Google LLC',          'ML Research Intern',          'Research role working on NLP models. Knowledge of TensorFlow and research paper reading required.',                      'Internship', 'https://careers.google.com',    'Remote',              '2026-12-31'),
(7, 3, 'Qualcomm',            'Embedded Systems Intern',     'Hands-on internship with embedded Linux and ARM Cortex microcontrollers. C programming required.',                      'Internship', 'https://qualcomm.com/careers',  'Pune, India',         '2027-01-15'),
(8, 8, 'Samsung Electronics', 'VLSI Design Intern',          'Work on RTL design and verification using SystemVerilog. Ideal for ECE students with digital design knowledge.',        'Internship', 'https://samsung.com/in/careers','Noida, India',        '2026-11-20');

-- MENTORSHIP REQUESTS
INSERT IGNORE INTO Mentorship (mentorship_id, student_id, alumni_id, message, request_status, requested_at) VALUES
(1, 1, 1, 'Hi Alice! I am a 3rd year CSE student interested in software development at top companies. Could you guide me on interview prep and resume building?', 'Accepted',  '2026-10-01 10:00:00'),
(2, 2, 2, 'Hello Bob, I would love guidance on cloud computing and certifications to pursue as a 2nd year student.',                                               'Pending',   '2026-10-05 11:30:00'),
(3, 3, 3, 'Hi Carol, I am pursuing ECE and interested in embedded systems. Any advice on getting started?',                                                        'Accepted',  '2026-09-28 09:00:00'),
(4, 4, 7, 'Hello Grace, I am a 3rd year Mechanical student and am very interested in AutoCAD and design. Could you mentor me?',                                   'Rejected',  '2026-10-10 14:00:00'),
(5, 5, 5, 'Hi Eve, I am a business student fascinated by consulting. Can you share your journey to McKinsey?',                                                    'Pending',   '2026-10-15 16:45:00');

-- EVENTS
INSERT IGNORE INTO Event (event_id, event_name, description, event_date, venue, created_by) VALUES
(1, 'Annual Alumni Meet 2026',        'Reconnect with batchmates and network with industry leaders from top companies.', '2026-12-15', 'University Main Auditorium',      1),
(2, 'Career Development Webinar',     'Interactive webinar on resume building, interview tips, and career planning for final year students.', '2026-11-10', 'Online - Zoom', 1),
(3, 'Startup Pitch Competition 2026', 'Present your startup idea to a panel of alumni investors and mentors.', '2026-11-25', 'Innovation Lab, Block C',          2);

-- EVENT REGISTRATIONS
INSERT IGNORE INTO Event_Registration (event_id, user_id, registration_date, attendance_status) VALUES
(1, 2,  '2026-10-15 10:00:00', 'Registered'),
(1, 3,  '2026-10-16 11:00:00', 'Registered'),
(1, 12, '2026-10-17 09:30:00', 'Registered'),
(1, 13, '2026-10-18 14:00:00', 'Registered'),
(2, 12, '2026-10-20 10:00:00', 'Registered'),
(2, 14, '2026-10-20 11:00:00', 'Registered'),
(2, 4,  '2026-10-21 09:00:00', 'Registered'),
(3, 6,  '2026-10-19 13:00:00', 'Registered'),
(3, 16, '2026-10-20 15:00:00', 'Registered');
