#!/usr/bin/env python3
"""
setup_local_db.py - Pre-populates the local database with all synthetic data.
This guarantees that departments, alumni, jobs, and events are ALWAYS visible
even before MySQL is configured!
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alumni_management.sqlite3')

def populate_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create Tables
    cursor.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS Department (
        department_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS Users (
        user_id        INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name      TEXT NOT NULL,
        email          TEXT NOT NULL UNIQUE,
        password_hash  TEXT NOT NULL,
        role           TEXT NOT NULL CHECK(role IN ('admin', 'alumni', 'student')),
        account_status TEXT NOT NULL DEFAULT 'pending' CHECK(account_status IN ('pending', 'approved', 'rejected')),
        created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS Alumni (
        alumni_id       INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id         INTEGER NOT NULL UNIQUE,
        department_id   INTEGER NOT NULL,
        graduation_year INTEGER NOT NULL,
        current_company TEXT,
        job_title       TEXT,
        skills          TEXT,
        linkedin_url    TEXT,
        bio             TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (department_id) REFERENCES Department(department_id)
    );

    CREATE TABLE IF NOT EXISTS Student (
        student_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id       INTEGER NOT NULL UNIQUE,
        department_id INTEGER NOT NULL,
        current_year  INTEGER NOT NULL,
        skills        TEXT,
        interests     TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
        FOREIGN KEY (department_id) REFERENCES Department(department_id)
    );

    CREATE TABLE IF NOT EXISTS Job (
        job_id           INTEGER PRIMARY KEY AUTOINCREMENT,
        alumni_id        INTEGER NOT NULL,
        company_name     TEXT NOT NULL,
        job_title        TEXT NOT NULL,
        job_description  TEXT NOT NULL,
        job_type         TEXT NOT NULL,
        application_link TEXT,
        location         TEXT,
        deadline         DATE,
        created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (alumni_id) REFERENCES Alumni(alumni_id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Mentorship (
        mentorship_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id     INTEGER NOT NULL,
        alumni_id      INTEGER NOT NULL,
        message        TEXT,
        request_status TEXT NOT NULL DEFAULT 'Pending',
        requested_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
        FOREIGN KEY (alumni_id)  REFERENCES Alumni(alumni_id) ON DELETE CASCADE,
        UNIQUE (student_id, alumni_id)
    );

    CREATE TABLE IF NOT EXISTS Event (
        event_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name  TEXT NOT NULL,
        description TEXT,
        event_date  DATE NOT NULL,
        venue       TEXT,
        created_by  INTEGER NOT NULL,
        FOREIGN KEY (created_by) REFERENCES Users(user_id)
    );

    CREATE TABLE IF NOT EXISTS Event_Registration (
        registration_id   INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id          INTEGER NOT NULL,
        user_id           INTEGER NOT NULL,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        attendance_status TEXT NOT NULL DEFAULT 'Registered',
        FOREIGN KEY (event_id) REFERENCES Event(event_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id)  REFERENCES Users(user_id) ON DELETE CASCADE,
        UNIQUE (event_id, user_id)
    );

    -- Views
    CREATE VIEW IF NOT EXISTS alumni_directory_view AS
    SELECT
        a.alumni_id, u.full_name, u.email, d.department_name,
        a.graduation_year, a.current_company, a.job_title,
        a.skills, a.linkedin_url, a.bio, u.account_status
    FROM Alumni a
    JOIN Users u ON a.user_id = u.user_id
    JOIN Department d ON a.department_id = d.department_id
    WHERE u.account_status = 'approved';

    CREATE VIEW IF NOT EXISTS job_opportunities_view AS
    SELECT
        j.job_id, j.company_name, j.job_title, j.job_description,
        j.job_type, j.application_link, j.location, j.deadline, j.created_at,
        u.full_name AS posted_by, d.department_name AS alumni_department
    FROM Job j
    JOIN Alumni a ON j.alumni_id = a.alumni_id
    JOIN Users u ON a.user_id = u.user_id
    JOIN Department d ON a.department_id = d.department_id
    WHERE u.account_status = 'approved';
    """)

    # 2. Insert Departments (if empty)
    cursor.execute("SELECT COUNT(*) FROM Department")
    if cursor.fetchone()[0] == 0:
        departments = [
            (1, 'Computer Science Engineering'),
            (2, 'Electronics & Communication Engineering'),
            (3, 'Mechanical Engineering'),
            (4, 'Civil Engineering'),
            (5, 'Information Technology & Data Science')
        ]
        cursor.executemany("INSERT INTO Department VALUES (?, ?)", departments)

    # 3. Insert Users & Profiles
    cursor.execute("SELECT COUNT(*) FROM Users")
    if cursor.fetchone()[0] == 0:
        admin_hash   = generate_password_hash("Admin@1234")
        alumni_hash  = generate_password_hash("Alumni@1234")
        student_hash = generate_password_hash("Student@1234")

        users = [
            (1, 'System Administrator', 'admin@alumni.example.com', admin_hash, 'admin', 'approved'),
            (2, 'Alice Johnson', 'alice.johnson@example.com', alumni_hash, 'alumni', 'approved'),
            (3, 'Bob Smith', 'bob.smith@example.com', alumni_hash, 'alumni', 'approved'),
            (4, 'Carol White', 'carol.white@example.com', alumni_hash, 'alumni', 'approved'),
            (5, 'David Lee', 'david.lee@example.com', alumni_hash, 'alumni', 'approved'),
            (6, 'Eve Martin', 'eve.martin@example.com', alumni_hash, 'alumni', 'approved'),
            (7, 'Frank Chen', 'frank.chen@example.com', alumni_hash, 'alumni', 'approved'),
            (8, 'Grace Patel', 'grace.patel@example.com', alumni_hash, 'alumni', 'approved'),
            (9, 'James Davis', 'james.davis@example.com', alumni_hash, 'alumni', 'pending'),
            (10, 'Kate Brown', 'kate.brown@example.com', student_hash, 'student', 'approved'),
            (11, 'Liam Jones', 'liam.jones@example.com', student_hash, 'student', 'approved'),
            (12, 'Mia Taylor', 'mia.taylor@example.com', student_hash, 'student', 'approved'),
            (13, 'Noah Wilson', 'noah.wilson@example.com', student_hash, 'student', 'approved')
        ]
        cursor.executemany("INSERT INTO Users (user_id, full_name, email, password_hash, role, account_status) VALUES (?,?,?,?,?,?)", users)

        # Alumni
        alumni = [
            (1, 2, 1, 2020, 'Google LLC', 'Senior Software Engineer', 'Python, Go, Kubernetes, Cloud', 'https://linkedin.com/in/alice', 'Passionate about cloud architectures and backend engineering.'),
            (2, 3, 1, 2019, 'Microsoft', 'Data Architect', 'Azure, SQL, Data Warehousing, PowerBI', 'https://linkedin.com/in/bob', 'Helping enterprises build reliable data lakes.'),
            (3, 4, 2, 2021, 'Qualcomm', 'Hardware Design Engineer', 'VLSI, Verilog, FPGA, C++', 'https://linkedin.com/in/carol', 'Specialized in 5G chip architecture and low-power circuits.'),
            (4, 5, 5, 2022, 'Amazon AWS', 'DevOps & SRE Engineer', 'Linux, Docker, Terraform, CI/CD', 'https://linkedin.com/in/david', 'Automating deployments and high availability systems.'),
            (5, 6, 3, 2018, 'Tesla / Tata Motors', 'R&D Design Engineer', 'AutoCAD, SolidWorks, Simulation, EV', 'https://linkedin.com/in/eve', 'Focused on Electric Vehicle battery pack thermals.'),
            (6, 7, 1, 2023, 'Flipkart', 'Backend Engineer', 'Java, Spring Boot, Kafka, MySQL', 'https://linkedin.com/in/frank', 'E-commerce checkout systems and transaction processing.'),
            (7, 8, 4, 2017, 'L&T Construction', 'Project Manager', 'Primavera, Structural Design, BIM', 'https://linkedin.com/in/grace', 'Infrastructure and metro rail transit projects.'),
            (8, 9, 1, 2024, 'Startup Hub', 'Junior Developer', 'Python, Flask, React', None, 'Recent graduate awaiting admin review.')
        ]
        cursor.executemany("INSERT INTO Alumni VALUES (?,?,?,?,?,?,?,?,?)", alumni)

        # Students
        students = [
            (1, 10, 1, 3, 'Python, SQL, HTML/CSS', 'Full-stack Web Dev, Database Design'),
            (2, 11, 2, 2, 'C++, Arduino, Embedded Systems', 'IoT and Robotics'),
            (3, 12, 5, 4, 'Machine Learning, Pandas, R', 'Data Science & Predictive Analytics'),
            (4, 13, 3, 3, 'AutoCAD, ANSYS, MATLAB', 'Automotive & CAD Modeling')
        ]
        cursor.executemany("INSERT INTO Student VALUES (?,?,?,?,?,?)", students)

        # Jobs
        jobs = [
            (1, 1, 'Google LLC', 'Software Engineer Intern (Summer 2027)', 'Join Google engineering teams to build distributed services. Open to 3rd & 4th year students.', 'Internship', 'https://careers.google.com', 'Bengaluru / Remote', '2027-03-31'),
            (2, 2, 'Microsoft', 'Data Platform Engineer', 'Work on Azure cloud data pipelines. Experience with SQL and Python required.', 'Full-time', 'https://careers.microsoft.com', 'Hyderabad, India', '2027-01-15'),
            (3, 3, 'Qualcomm', 'VLSI Design Intern', 'Hands-on RTL synthesis and testing of microcontroller blocks.', 'Internship', 'https://qualcomm.com/careers', 'Bengaluru, India', '2026-12-30'),
            (4, 4, 'Amazon AWS', 'Cloud Support Associate', 'Support enterprise customers deploying infrastructure on AWS EC2 & RDS.', 'Full-time', 'https://amazon.jobs', 'Pune / Remote', '2027-02-28'),
            (5, 6, 'Flipkart', 'Junior Backend Developer', 'Build high-throughput REST APIs using Java and MySQL.', 'Full-time', 'https://flipkart.com', 'Bengaluru, India', '2027-02-15')
        ]
        cursor.executemany("INSERT INTO Job (job_id, alumni_id, company_name, job_title, job_description, job_type, application_link, location, deadline) VALUES (?,?,?,?,?,?,?,?,?)", jobs)

        # Mentorship Requests
        mentorships = [
            (1, 1, 1, 'Hi Alice! I am a 3rd year student interested in backend systems. Would love your guidance on resume and interview preparation.', 'Accepted'),
            (2, 2, 3, 'Hello Carol, can you give tips for cracking hardware/VLSI campus placements?', 'Accepted'),
            (3, 3, 2, 'Dear Bob, I would love to learn more about data engineering roadmaps.', 'Pending'),
            (4, 4, 5, 'Hi Eve, I am interested in CAD design roles in automotive companies.', 'Pending')
        ]
        cursor.executemany("INSERT INTO Mentorship (mentorship_id, student_id, alumni_id, message, request_status) VALUES (?,?,?,?,?)", mentorships)

        # Events
        events = [
            (1, 'Annual Alumni Homecoming & Networking 2026', 'Connect with alumni working at top tech and core engineering companies.', '2026-12-20', 'College Main Auditorium', 1),
            (2, 'Masterclass: Cracking Tech Interviews', 'Interactive session on Data Structures, System Design, and Resume Building.', '2026-11-15', 'Virtual (Google Meet)', 1),
            (3, 'Higher Studies & MS in USA / Europe Webinar', 'Alumni sharing their experiences with GRE, scholarships, and universities.', '2026-11-28', 'Seminar Hall 2', 1)
        ]
        cursor.executemany("INSERT INTO Event VALUES (?,?,?,?,?,?)", events)

        # Event Registrations
        registrations = [
            (1, 1, 10, 'Registered'),
            (2, 1, 11, 'Registered'),
            (3, 2, 10, 'Registered'),
            (4, 2, 12, 'Registered')
        ]
        cursor.executemany("INSERT INTO Event_Registration (registration_id, event_id, user_id, attendance_status) VALUES (?,?,?,?)", registrations)

    conn.commit()
    conn.close()
    print("✅ Local database successfully populated with all departments, users, alumni, and jobs!")

if __name__ == '__main__':
    populate_database()
