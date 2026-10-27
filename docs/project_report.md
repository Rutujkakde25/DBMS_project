# 🎓 Project Report: Alumni Networking Management System

**Course:** Database Management Systems (DBMS) Mini Project  
**Domain:** Web Application & Relational Database Design  
**Tech Stack:** Python Flask, MySQL, HTML5, CSS3, JavaScript  

---

## 1. Abstract
The Alumni Networking Management System provides an integrated online platform connecting university students with alumni. It simplifies alumni record maintenance, job and internship discovery, event registrations, and 1-on-1 career mentorship. The system addresses the common college problem of fragmented alumni records and disconnected professional networks.

---

## 2. Problem Statement
Most colleges lose direct connection with graduates, leaving current students without industry access, mentorship, or verifiable referral pipelines. Manual directory updates (spreadsheets) are prone to data inconsistencies, lost records, and security issues.

---

## 3. Objectives
- Centralize alumni, student, and department information using a normalized relational schema.
- Implement Role-Based Access Control (RBAC) separating Admin, Alumni, and Student privileges.
- Implement verification workflows (admin approves alumni before they can log in).
- Facilitate direct student-to-alumni mentorship requests without duplicate spamming.
- Enable alumni to publish internships and job openings with deadline tracking.
- Ensure SQL injection prevention using parameterized prepared statements.

---

## 4. System Architecture & Relational Design

### Schema Overview (8 Tables)
1. **Department**: University departments (`department_id`, `department_name`).
2. **Users**: Central user authentication table (`user_id`, `email`, `password_hash`, `role`, `account_status`, `created_at`).
3. **Alumni**: Detailed alumni profile (`alumni_id`, `user_id`, `department_id`, `graduation_year`, `current_company`, `job_title`, `skills`, `linkedin_url`, `bio`).
4. **Student**: Current student profile (`student_id`, `user_id`, `department_id`, `current_year`, `skills`, `interests`).
5. **Job**: Opportunities posted by alumni (`job_id`, `alumni_id`, `company_name`, `job_title`, `job_description`, `job_type`, `location`, `deadline`).
6. **Mentorship**: Student-Alumni mentorship requests (`mentorship_id`, `student_id`, `alumni_id`, `message`, `request_status`, `requested_at`).
7. **Event**: Campus & webinar events (`event_id`, `event_name`, `description`, `event_date`, `venue`, `created_by`).
8. **Event_Registration**: Junction table (`registration_id`, `event_id`, `user_id`, `registration_date`, `attendance_status`).

---

## 5. DBMS Features Demonstrated
- **Normalization:** Evaluated across 1NF, 2NF, and 3NF.
- **Constraints:** Primary Keys, Foreign Keys (`ON DELETE CASCADE`), `UNIQUE(email)`, `UNIQUE(event_id, user_id)`, `UNIQUE(student_id, alumni_id)`.
- **Joins:** INNER JOIN, LEFT JOIN, Multi-table joins across 4+ tables.
- **Aggregations & Subqueries:** `COUNT()`, `GROUP BY`, `HAVING` with nested scalar average subquery.
- **Views:** `alumni_directory_view`, `job_opportunities_view`.
- **Stored Procedure:** `GetAlumniByFilter(p_department_id, p_graduation_year)`.
- **Trigger:** `trg_validate_mentorship` to prevent mentorship requests to non-approved accounts.
- **Transactions:** Python `conn.start_transaction()` ensuring both User record and role profile are committed atomically.

---

## 6. Screenshots Checklist for Project File
- [ ] Home Page with Network Statistics
- [ ] Login & Role-based Registration Form
- [ ] Admin Dashboard (Statistics Cards & Department Bar Chart)
- [ ] Admin Alumni Approval & Management Screen
- [ ] Alumni Dashboard & Profile Editor
- [ ] Alumni Job Posting Form
- [ ] Student Search Alumni with Filter Controls
- [ ] Student Mentorship Request Submission & Status Screen
- [ ] Event Registration Interface

---

## 7. Limitations & Future Scope
- **Current Limitations:** Email notifications are simulated in-app; resume upload is link-based.
- **Future Scope:** Resume PDF storage via AWS S3 / local file storage, automated password reset tokens via SMTP, live chat messaging between accepted mentor and student.
