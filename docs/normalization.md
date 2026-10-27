# Database Normalization – Alumni Networking Management System

## What is Normalization?

Database normalization is the process of structuring a relational database to reduce data redundancy and improve data integrity. It involves organizing columns and tables to satisfy normal forms (NF).

---

## 1NF – First Normal Form

**Rules:**
1. Each column holds atomic (indivisible) values.
2. Each row is unique (identified by a primary key).
3. No repeating groups.

**Verification:**

| Table | Atomic Values? | Primary Key? | No Repeating Groups? |
|---|---|---|---|
| Department | ✅ `department_name` is a single string | ✅ `department_id` | ✅ |
| Users | ✅ Each column stores one value | ✅ `user_id` | ✅ |
| Alumni | ✅ `skills` is stored as comma-separated text (one field, not multiple columns) | ✅ `alumni_id` | ✅ |
| Student | ✅ | ✅ `student_id` | ✅ |
| Job | ✅ | ✅ `job_id` | ✅ |
| Mentorship | ✅ | ✅ `mentorship_id` | ✅ |
| Event | ✅ | ✅ `event_id` | ✅ |
| Event_Registration | ✅ | ✅ `registration_id` | ✅ |

**All tables satisfy 1NF.**

> Note: `skills` and `interests` are stored as TEXT (comma-separated) for simplicity. In a higher-normalization design, these could be split into separate `Skills` and `Alumni_Skills` tables. For this project scope, TEXT is acceptable and the table still satisfies 1NF because the column itself is atomic from the database's perspective.

---

## 2NF – Second Normal Form

**Rules:**
1. Must be in 1NF.
2. Every non-key attribute must be **fully functionally dependent** on the entire primary key (no partial dependencies). This applies only to tables with composite primary keys.

**Functional Dependencies:**

### Department
- `department_id → department_name`
- Only one attribute; fully dependent on PK. ✅

### Users
- `user_id → full_name, email, password_hash, role, account_status, created_at`
- All attributes depend fully on `user_id`. ✅

### Alumni
- `alumni_id → user_id, department_id, graduation_year, current_company, job_title, skills, linkedin_url, bio`
- All attributes fully depend on `alumni_id`. ✅
- No composite primary key → 2NF automatically satisfied.

### Mentorship
- Primary key: `mentorship_id` (single column)
- `mentorship_id → student_id, alumni_id, message, request_status, requested_at`
- All attributes fully depend on `mentorship_id`. ✅

### Event_Registration
- Primary key: `registration_id` (single column)
- `registration_id → event_id, user_id, registration_date, attendance_status`
- Fully functionally dependent on `registration_id`. ✅
- The UNIQUE(event_id, user_id) is a candidate key but not the PK; no partial dependency exists.

**All tables satisfy 2NF.**

---

## 3NF – Third Normal Form

**Rules:**
1. Must be in 2NF.
2. No **transitive dependencies** – non-key attributes must not depend on other non-key attributes.

**Checking for Transitive Dependencies:**

### Users
- Does `role` determine `account_status`? No — `account_status` is independently set by admin. ✅
- No transitive dependencies.

### Alumni
- Does `current_company → job_title`? Not in our schema — they are independent attributes.
- Does `department_id` depend on another non-key column? No — it's a FK, not derived from other columns. ✅
- `department_name` is NOT stored in Alumni; it is accessed via JOIN with Department. ✅

### Job
- Does `company_name` determine `location`? Not enforced — same company could have multiple locations. ✅
- All attributes depend directly on `job_id`, not on other non-key attributes.

### Mentorship
- `request_status` depends on `mentorship_id`, not on `student_id` or `alumni_id`. ✅

**All tables satisfy 3NF.**

---

## Why Junction Tables?

### Event_Registration
Events and Users have a **many-to-many** relationship:
- One event can have many registrants.
- One user can register for many events.

Without a junction table, we would need to store either:
- Multiple user_ids in one Event row (violates 1NF), or
- Multiple event_ids in one User row (violates 1NF).

The `Event_Registration` table resolves this by storing one row per (event, user) pair, with additional attributes like `registration_date` and `attendance_status` that belong to the relationship itself.

---

## Primary Keys Summary

| Table | Primary Key | Type |
|---|---|---|
| Department | department_id | INT AUTO_INCREMENT |
| Users | user_id | INT AUTO_INCREMENT |
| Alumni | alumni_id | INT AUTO_INCREMENT |
| Student | student_id | INT AUTO_INCREMENT |
| Job | job_id | INT AUTO_INCREMENT |
| Mentorship | mentorship_id | INT AUTO_INCREMENT |
| Event | event_id | INT AUTO_INCREMENT |
| Event_Registration | registration_id | INT AUTO_INCREMENT |

## Foreign Keys Summary

| Table | Foreign Key | References |
|---|---|---|
| Alumni | user_id | Users(user_id) |
| Alumni | department_id | Department(department_id) |
| Student | user_id | Users(user_id) |
| Student | department_id | Department(department_id) |
| Job | alumni_id | Alumni(alumni_id) |
| Mentorship | student_id | Student(student_id) |
| Mentorship | alumni_id | Alumni(alumni_id) |
| Event | created_by | Users(user_id) |
| Event_Registration | event_id | Event(event_id) |
| Event_Registration | user_id | Users(user_id) |
