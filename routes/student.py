from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from database.db_connection import execute_query
from functools import wraps

student_bp = Blueprint('student', __name__, url_prefix='/student')

def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'student':
            # Auto-assign Student session for instant demo!
            session['user_id'] = 10
            session['full_name'] = 'Kate Brown (Demo Student)'
            session['role'] = 'student'
            session['email'] = 'kate.brown@example.com'
        return f(*args, **kwargs)
    return decorated

def get_student_profile(user_id):
    row = execute_query("SELECT * FROM Student WHERE user_id=%s", (user_id,), fetchone=True)
    if not row:
        row = execute_query("SELECT * FROM Student LIMIT 1", fetchone=True)
    return row


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
@student_bp.route('/')
@student_required
def dashboard():
    profile = get_student_profile(session['user_id'])
    student_id = profile['student_id'] if profile else 1

    jobs_count = execute_query("SELECT COUNT(*) AS cnt FROM Job", fetchone=True)
    alumni_count = execute_query("SELECT COUNT(*) AS cnt FROM Alumni a JOIN Users u ON a.user_id=u.user_id WHERE u.account_status='approved'", fetchone=True)
    my_requests = execute_query("SELECT COUNT(*) AS cnt FROM Mentorship WHERE student_id=%s", (student_id,), fetchone=True)
    events_count = execute_query("SELECT COUNT(*) AS cnt FROM Event", fetchone=True)

    recent_jobs = execute_query("""
        SELECT j.job_title, j.company_name, j.job_type, j.location, j.deadline, j.job_id
        FROM Job j ORDER BY j.created_at DESC LIMIT 4
    """, fetch=True) or []

    return render_template('student/dashboard.html',
                           profile=profile or {},
                           jobs_count=jobs_count['cnt'] if jobs_count else 0,
                           alumni_count=alumni_count['cnt'] if alumni_count else 0,
                           my_requests=my_requests['cnt'] if my_requests else 0,
                           events_count=events_count['cnt'] if events_count else 0,
                           recent_jobs=recent_jobs)


# ─────────────────────────────────────────────
# EDIT PROFILE
# ─────────────────────────────────────────────
@student_bp.route('/profile', methods=['GET', 'POST'])
@student_required
def edit_profile():
    profile = get_student_profile(session['user_id'])
    departments = execute_query("SELECT * FROM Department ORDER BY department_name", fetch=True) or []

    if request.method == 'POST':
        full_name  = request.form.get('full_name', '').strip()
        dept_id    = request.form.get('department_id', 1)
        curr_year  = request.form.get('current_year', 3)
        skills     = request.form.get('skills', '').strip()
        interests  = request.form.get('interests', '').strip()

        execute_query("UPDATE Users SET full_name=%s WHERE user_id=%s", (full_name, session['user_id']))
        execute_query("""
            UPDATE Student SET department_id=%s, current_year=%s, skills=%s, interests=%s
            WHERE user_id=%s
        """, (dept_id, curr_year, skills, interests, session['user_id']))
        session['full_name'] = full_name
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('student.edit_profile'))

    user = execute_query("SELECT full_name, email FROM Users WHERE user_id=%s", (session['user_id'],), fetchone=True)
    return render_template('student/edit_profile.html', profile=profile, departments=departments, user=user or {'full_name': 'Kate Brown', 'email': 'kate@example.com'})


# ─────────────────────────────────────────────
# SEARCH ALUMNI
# ─────────────────────────────────────────────
@student_bp.route('/search-alumni')
@student_required
def search_alumni():
    name      = request.args.get('name', '').strip()
    dept_id   = request.args.get('department_id', '')
    grad_year = request.args.get('graduation_year', '').strip()
    company   = request.args.get('company', '').strip()
    skills    = request.args.get('skills', '').strip()

    query = """
        SELECT a.alumni_id, u.full_name, d.department_name,
               a.graduation_year, a.current_company, a.job_title,
               a.skills, a.linkedin_url, a.bio
        FROM Alumni a
        INNER JOIN Users u ON a.user_id = u.user_id
        INNER JOIN Department d ON a.department_id = d.department_id
        WHERE u.account_status = 'approved'
    """
    params = []

    if name:
        query += " AND u.full_name LIKE %s"
        params.append(f'%{name}%')
    if dept_id:
        query += " AND a.department_id = %s"
        params.append(dept_id)
    if grad_year:
        query += " AND a.graduation_year = %s"
        params.append(grad_year)
    if company:
        query += " AND a.current_company LIKE %s"
        params.append(f'%{company}%')
    if skills:
        query += " AND a.skills LIKE %s"
        params.append(f'%{skills}%')

    query += " ORDER BY u.full_name ASC"

    alumni_list = execute_query(query, tuple(params), fetch=True) or []
    departments = execute_query("SELECT * FROM Department ORDER BY department_name", fetch=True) or []
    profile = get_student_profile(session['user_id'])

    already_sent = set()
    if profile:
        sent = execute_query("SELECT alumni_id FROM Mentorship WHERE student_id=%s", (profile['student_id'],), fetch=True) or []
        already_sent = {row['alumni_id'] for row in sent}

    return render_template('student/search_alumni.html',
                           alumni_list=alumni_list,
                           departments=departments,
                           already_sent=already_sent,
                           filters={'name': name, 'dept_id': dept_id, 'grad_year': grad_year,
                                    'company': company, 'skills': skills})


# ─────────────────────────────────────────────
# JOBS
# ─────────────────────────────────────────────
@student_bp.route('/jobs')
@student_required
def browse_jobs():
    job_type = request.args.get('job_type', '')
    query = "SELECT * FROM job_opportunities_view WHERE 1=1"
    params = []
    if job_type:
        query += " AND job_type=%s"
        params.append(job_type)
    query += " ORDER BY created_at DESC"
    jobs = execute_query(query, tuple(params), fetch=True) or []
    return render_template('student/browse_jobs.html', jobs=jobs, job_type=job_type)


# ─────────────────────────────────────────────
# MENTORSHIP
# ─────────────────────────────────────────────
@student_bp.route('/mentorship/send/<int:alumni_id>', methods=['POST'])
@student_required
def send_mentorship(alumni_id):
    profile = get_student_profile(session['user_id'])
    student_id = profile['student_id'] if profile else 1
    message = request.form.get('message', 'Hi, I would love to connect for mentorship!').strip()

    execute_query("""
        INSERT INTO Mentorship (student_id, alumni_id, message)
        VALUES (%s, %s, %s)
    """, (student_id, alumni_id, message))

    flash('Mentorship request sent successfully!', 'success')
    return redirect(url_for('student.my_mentorship'))


@student_bp.route('/mentorship')
@student_required
def my_mentorship():
    profile = get_student_profile(session['user_id'])
    student_id = profile['student_id'] if profile else 1
    requests_list = execute_query("""
        SELECT m.mentorship_id, m.message, m.request_status, m.requested_at,
               u.full_name AS alumni_name, u.email AS alumni_email,
               a.current_company, a.job_title, d.department_name
        FROM Mentorship m
        JOIN Alumni a ON m.alumni_id = a.alumni_id
        JOIN Users u ON a.user_id = u.user_id
        JOIN Department d ON a.department_id = d.department_id
        WHERE m.student_id=%s
        ORDER BY m.requested_at DESC
    """, (student_id,), fetch=True) or []
    return render_template('student/my_mentorship.html', requests=requests_list)


# ─────────────────────────────────────────────
# EVENTS
# ─────────────────────────────────────────────
@student_bp.route('/events')
@student_required
def browse_events():
    events = execute_query("""
        SELECT e.event_id, e.event_name, e.description, e.event_date, e.venue,
               u.full_name AS organizer,
               COUNT(er.registration_id) AS reg_count
        FROM Event e
        JOIN Users u ON e.created_by = u.user_id
        LEFT JOIN Event_Registration er ON e.event_id = er.event_id
        GROUP BY e.event_id
        ORDER BY e.event_date ASC
    """, fetch=True) or []

    registered = execute_query("SELECT event_id FROM Event_Registration WHERE user_id=%s", (session.get('user_id', 10),), fetch=True) or []
    registered_ids = {row['event_id'] for row in registered}

    return render_template('student/browse_events.html', events=events, registered_ids=registered_ids)


@student_bp.route('/events/register/<int:event_id>', methods=['POST'])
@student_required
def register_event(event_id):
    user_id = session.get('user_id', 10)
    execute_query("INSERT OR IGNORE INTO Event_Registration (event_id, user_id) VALUES (%s, %s)", (event_id, user_id))
    flash('Successfully registered for the event!', 'success')
    return redirect(url_for('student.browse_events'))
