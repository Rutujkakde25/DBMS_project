# 🗣️ DBMS Viva Questions & Answers (Alumni Networking Project)

These 15 questions and answers are tailored specifically to this project's database schema, MySQL queries, and architecture for oral exams.

---

### Q1: What is the purpose of the `Users` table instead of having separate tables for each role?
**Ans:** By using a centralized `Users` table, we avoid duplicate authentication columns (email, password hash, status) across multiple tables. This enforces email uniqueness universally across the portal and simplifies authentication logic while adhering to normalization.

---

### Q2: What normal forms does your schema satisfy?
**Ans:** It satisfies **1NF, 2NF, and 3NF**:
- **1NF:** All attributes hold atomic values and each table has an explicit Primary Key.
- **2NF:** There are no partial functional dependencies (all non-key columns depend on the full primary key).
- **3NF:** There are no transitive dependencies; non-key attributes do not determine other non-key attributes (e.g., department name is stored in `Department`, referenced by foreign key).

---

### Q3: Why is `Event_Registration` modeled as a separate junction table?
**Ans:** Because there is a **many-to-many (M:N)** relationship between `Users` and `Events`. One user can register for multiple events, and one event can have multiple attendees. The junction table resolves this and includes relationship attributes like `registration_date` and `attendance_status`.

---

### Q4: How do you prevent a student from registering twice for the same event?
**Ans:** We added a composite `UNIQUE(event_id, user_id)` constraint on the `Event_Registration` table at the database level, as well as an active validation check in the Flask route.

---

### Q5: What is the difference between `INNER JOIN` and `LEFT JOIN` in your project?
**Ans:** 
- `INNER JOIN` is used when we only want records that match in both tables (e.g., displaying approved alumni with their department name).
- `LEFT JOIN` is used when we want all records from the left table regardless of whether matches exist on the right (e.g., finding students who have **never** sent a mentorship request, where `Mentorship.mentorship_id IS NULL`).

---

### Q6: What does the `ON DELETE CASCADE` constraint do in your schema?
**Ans:** When a record in a parent table is deleted (e.g., deleting a User record from `Users`), MySQL automatically removes all linked records in child tables (`Alumni`, `Student`, `Job`, `Mentorship`) to maintain referential integrity without orphan records.

---

### Q7: What stored procedure did you implement and why?
**Ans:** We created `GetAlumniByFilter(p_department_id, p_graduation_year)`. It encapsulates the complex query filtering alumni by department and batch year directly on the database engine, reducing network overhead and improving execution speed.

---

### Q8: What trigger did you write in MySQL?
**Ans:** We wrote `trg_validate_mentorship` on `BEFORE INSERT` on the `Mentorship` table. It checks if the recipient alumnus has `account_status = 'approved'`. If not, it signals SQLSTATE `'45000'` with an error message, aborting the insert at the database engine level.

---

### Q9: Why did you create SQL Views (`alumni_directory_view`, `job_opportunities_view`)?
**Ans:** Views provide a virtual table layer that:
1. Simplifies complex multi-table joins into a reusable SELECT query.
2. Enhances security by restricting exposure of sensitive columns (such as `password_hash`).

---

### Q10: How does your application protect against SQL Injection?
**Ans:** We do not concatenate variables into raw SQL strings. Every query uses **parameterized queries** with `%s` placeholders handled by `mysql-connector-python`, ensuring user input is treated strictly as data and never executed as executable SQL.

---

### Q11: How do you handle password security?
**Ans:** Passwords are never stored in plain text. They are hashed using **PBKDF2 with SHA-256** and salt using Werkzeug's `generate_password_hash()`. When logging in, `check_password_hash()` compares the hash.

---

### Q12: Why did you use database transactions during registration?
**Ans:** Registration requires writing to two tables: `Users` (to create the account) and `Alumni` or `Student` (to create the role-specific profile). Using `conn.start_transaction()` ensures that if the second insert fails, the first is rolled back, preventing orphaned or incomplete user accounts (Atomicity in ACID).

---

### Q13: What indexes did you create and why?
**Ans:** Indexes were created on `Users(email)` (frequent login lookups), `Alumni(department_id)` and `Alumni(graduation_year)` (frequent search filter queries), and foreign keys to accelerate JOIN operations.

---

### Q14: Explain the subquery you wrote using `HAVING`.
**Ans:** In `database/queries.sql`, we group alumni by department and use `HAVING alumni_count > (SELECT AVG(...) FROM ...)` to find only those departments whose total number of alumni exceeds the overall average across all departments.

---

### Q15: What is the difference between a Trigger and a Stored Procedure?
**Ans:** 
- A **Stored Procedure** is explicitly called by the application or developer using `CALL ProcedureName(...)`.
- A **Trigger** is automatically invoked by the database engine in response to an event (e.g., `BEFORE INSERT`, `AFTER UPDATE`) on a specified table.
