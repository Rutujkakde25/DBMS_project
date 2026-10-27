# 🎓 Alumni Networking Management System

A full-stack, normalized relational database web application built with **Python Flask**, **MySQL**, and modern **HTML/CSS/JS** for college DBMS project submissions.

---

## 🚀 Quick Start Guide (How to Run and See It)

### Step 1: Open Terminal & Navigate to Project
```bash
cd /home/rutuj25/Desktop/dexp/projdbms/alumni-management-system
```

### Step 2: Set Up Python Virtual Environment & Dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate    # On Linux/macOS
# or: venv\Scripts\activate # On Windows

# Install required packages
pip install -r requirements.txt
```

### Step 3: Configure Database Settings
Create your `.env` file from `.env.example`:
```bash
cp .env.example .env
```
Edit `.env` to match your local MySQL credentials:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=alumni_management
SECRET_KEY=secret_dev_key_12345
```

### Step 4: Initialize the MySQL Database & Seed Data
Run the SQL scripts in order using the MySQL CLI or MySQL Workbench:
```bash
# 1. Create database schema, tables, views, procedures, and trigger
mysql -u root -p < schema.sql

# 2. Populate realistic sample data (departments, alumni, students, jobs, events)
mysql -u root -p alumni_management < seed.sql
```

*(Optional helper script to verify password hashes)*:
```bash
python3 seed_hashes.py
```

### Step 5: Start the Flask Application
```bash
python3 app.py
```

### Step 6: View in Your Browser
Open your browser and navigate to:
👉 **`http://localhost:5000`**

---

## 🔑 Demo Login Accounts

| Role | Email Address | Password | Permissions & Actions |
|---|---|---|---|
| **Admin** | `admin@alumni.example.com` | `Admin@1234` | Full access: approve alumni, manage students/events/departments, view SQL analytics |
| **Alumni** | `alice.johnson@example.com` | `Alumni@1234` | Post & edit jobs, review mentorship requests, update professional profile |
| **Student** | `kate.brown@example.com` | `Student@1234` | Filter alumni by skill/company/year, send mentorship requests, browse & register for events |

*(More accounts are available in `seed.sql`)*

---

## 📂 Project Structure

```text
alumni-management-system/
├── app.py                      # Flask application factory & public routes
├── config.py                   # Configuration reader from environment
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── schema.sql                  # Complete MySQL DDL: 8 tables, indexes, views, procedure, trigger
├── seed.sql                    # Realistic seed dataset for demonstration
├── seed_hashes.py              # Script to generate & verify password hashes
├── README.md                   # Setup guide and instructions
│
├── database/
│   ├── db_connection.py        # MySQL connector with parameterized queries & transactions
│   ├── queries.sql             # Viva reference queries (Joins, Aggregates, Subqueries)
│   ├── views.sql               # SQL Views definitions
│   ├── procedures.sql          # Stored Procedure definitions
│   └── triggers.sql            # Trigger definitions
│
├── routes/
│   ├── auth.py                 # Registration, login, logout & transaction logic
│   ├── admin.py                # Admin dashboard, approvals, CRUD operations & analytics
│   ├── alumni.py               # Alumni profile management, job postings, mentorship handling
│   └── student.py              # Student dashboard, alumni filter search, mentorship, events
│
├── templates/
│   ├── base.html               # Master layout with responsive navbar, flash alerts & footer
│   ├── index.html              # Landing page with stats & call to action
│   ├── login.html              # Login interface with demo credentials box
│   ├── register.html           # Dynamic role-based registration form
│   ├── directory.html          # Public alumni directory preview
│   ├── about.html              # Project overview and DBMS concept showcase
│   ├── admin/                  # Admin dashboard, approvals, departments, events, reports
│   ├── alumni/                 # Alumni dashboard, profile editor, job management, mentorship
│   ├── student/                # Student dashboard, search filters, jobs, requests, events
│   └── errors/                 # 403, 404, and 500 error templates
│
├── static/
│   ├── css/style.css           # Custom modern, clean CSS portal styling
│   └── js/main.js              # Modal behavior, alerts auto-dismiss, form validation
│
└── docs/
    ├── ER_diagram.md           # Mermaid ER diagram with cardinalities & schema notes
    ├── normalization.md        # Comprehensive 1NF, 2NF, 3NF documentation
    ├── project_report.md       # Mini-project report for college submission
    └── viva_questions.md       # 15 detailed DBMS viva questions with answers
```

---

## 🛡️ Database & Security Features
- **Parameterized SQL Queries:** Prevents SQL injection via `mysql-connector-python`.
- **Role-Based Authorization:** Separate decorators ensuring students cannot access admin routes.
- **Transactions:** Atomic user registration ensuring User and Profile rows are created together.
- **Secure Password Hashing:** Salted hashes generated via PBKDF2:SHA256 (no plaintext passwords).
- **Referential Integrity:** Enforced via Foreign Keys with `ON DELETE CASCADE`.
# DBMS_project
