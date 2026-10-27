# ER Diagram – Alumni Networking Management System

## Entity-Relationship Diagram (Mermaid)

```mermaid
erDiagram
    Department {
        int department_id PK
        varchar department_name
    }

    Users {
        int user_id PK
        varchar full_name
        varchar email
        varchar password_hash
        enum role
        enum account_status
        datetime created_at
    }

    Alumni {
        int alumni_id PK
        int user_id FK
        int department_id FK
        year graduation_year
        varchar current_company
        varchar job_title
        text skills
        varchar linkedin_url
        text bio
    }

    Student {
        int student_id PK
        int user_id FK
        int department_id FK
        int current_year
        text skills
        text interests
    }

    Job {
        int job_id PK
        int alumni_id FK
        varchar company_name
        varchar job_title
        text job_description
        enum job_type
        varchar application_link
        varchar location
        date deadline
        datetime created_at
    }

    Mentorship {
        int mentorship_id PK
        int student_id FK
        int alumni_id FK
        text message
        enum request_status
        datetime requested_at
    }

    Event {
        int event_id PK
        varchar event_name
        text description
        date event_date
        varchar venue
        int created_by FK
    }

    Event_Registration {
        int registration_id PK
        int event_id FK
        int user_id FK
        datetime registration_date
        enum attendance_status
    }

    Department ||--o{ Alumni : "has"
    Department ||--o{ Student : "has"
    Users ||--|| Alumni : "has profile"
    Users ||--|| Student : "has profile"
    Alumni ||--o{ Job : "posts"
    Student ||--o{ Mentorship : "sends"
    Alumni ||--o{ Mentorship : "receives"
    Users ||--o{ Event_Registration : "registers for"
    Event ||--o{ Event_Registration : "has"
    Users ||--o{ Event : "creates"
```

## Relationships and Cardinalities

| Relationship | Type | Description |
|---|---|---|
| Department → Alumni | One-to-Many | One department has many alumni |
| Department → Student | One-to-Many | One department has many students |
| Users → Alumni | One-to-One | Each user has at most one alumni profile |
| Users → Student | One-to-One | Each user has at most one student profile |
| Alumni → Job | One-to-Many | One alumnus can post many jobs |
| Student → Mentorship | One-to-Many | One student can send many mentorship requests |
| Alumni → Mentorship | One-to-Many | One alumnus can receive many mentorship requests |
| Event → Event_Registration | One-to-Many | One event has many registrations |
| Users → Event_Registration | One-to-Many | One user can register for many events |
| Users → Event | One-to-Many | Admin/alumni can create multiple events |

## Notes

- The **UNIQUE constraint on (event_id, user_id)** in `Event_Registration` enforces that a user can register for each event only once, making it a proper junction table for a many-to-many relationship between Users and Events.
- The **UNIQUE constraint on (student_id, alumni_id)** in `Mentorship` ensures a student can only send one request to each alumnus.
- `Users` is the central authentication table; role-specific data is stored in `Alumni` or `Student` linked by `user_id`.
