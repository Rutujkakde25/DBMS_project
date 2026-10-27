from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from database.db_connection import execute_query
from functools import wraps

alumni_bp = Blueprint('alumni', __name__, url_prefix='/alumni')

def alumni_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'alumni':
            # Auto-assign Alumni session for instant demo!
            session['user_id'] = 2
            session['full_name'] = 'Alice Johnson (Demo Alumni)'
            session['role'] = 'alumni'
            session['email'] = 'alice.johnson@example.com'
        return f(*args, **kwargs)
    return decorated

def get_alumni_profile(user_id):
    row = execute_query("SELECT * FROM Alumni WHERE user_id=%s", (user_id,), fetchone=True)
    if not row:
        row = execute_query("SELECT * FROM Alumni LIMIT 1", fetchone=True)
    return row

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
@alumni_bp.route('/')
@alumni_required
def dashboard():
    profile = get_alumni_profile(session['user_id'])
    alumni_id = profile['alumni_id'] if profile else 1

    jobs = execute_query("SELECT COUNT(*) AS cnt FROM Job WHERE alumni_id=%s", (alumni_id,), fetchone=True)
    pending_m = execute_query("SELECT COUNT(*) AS cnt FROM Mentorship WHERE alumni_id=%s AND request_status='Pending'", (alumni_id,), fetchone=True)
    total_m   = execute_query("SELECT COUNT(*) AS cnt FROM Mentorship WHERE alumni_id=%s", (alumni_id,), fetchone=True)

    recent_jobs = execute_query("SELECT * FROM Job WHERE alumni_id=%s ORDER BY created_at DESC LIMIT 3", (alumni_id,), fetch=True) or []
    recent_req = execute_query("""
        SELECT m.mentorship_id, m.message, m.request_status, m.requested_at,
               u.full_name AS student_name, d.department_name, s.current_year
        FROM Mentorship m
        JOIN Student s ON m.student_id = s.student_id
        JOIN Users u ON s.user_id = u.user_id
        JOIN Department d ON s.department_id = d.department_id
        WHERE m.alumni_id=%s
        ORDER BY m.requested_at DESC LIMIT 3
    """, (alumni_id,), fetch=True) or []

    return render_template('alumni/dashboard.html',
                           profile=profile or {},
                           job_count=jobs['cnt'] if jobs else 0,
                           pending_mentorship=pending_m['cnt'] if pending_m else 0,
                           total_mentorship=total_m['cnt'] if total_m else 0,
                           recent_jobs=recent_jobs,
                           recent_req=recent_req)

# ─────────────────────────────────────────────
# EDIT PROFILE
# ─────────────────────────────────────────────
@alumni_bp.route('/profile', methods=['GET', 'POST'])
@alumni_required
def edit_profile():
    profile = get_alumni_profile(session['user_id'])
    departments = execute_query("SELECT * FROM Department ORDER BY department_name", fetch=True) or []

    if request.method == 'POST':
        company     = request.form.get('current_company', '').strip()
        job_title   = request.form.get('job_title', '').strip()
        skills      = request.form.get('skills', '').strip()
        linkedin    = request.form.get('linkedin_url', '').strip()
        bio         = request.form.get('bio', '').strip()
        dept_id     = request.form.get('department_id', 1)
        grad_year   = request.form.get('graduation_year', 2020)
        full_name   = request.form.get('full_name', '').strip()

        execute_query("UPDATE Users SET full_name=%s WHERE user_id=%s", (full_name, session['user_id']))
        execute_query("""
            UPDATE Alumni
            SET department_id=%s, graduation_year=%s, current_company=%s,
                job_title=%s, skills=%s, linkedin_url=%s, bio=%s
            WHERE user_id=%s
        """, (dept_id, grad_year, company, job_title, skills, linkedin, bio, session['user_id']))

        session['full_name'] = full_name
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('alumni.edit_profile'))

    user = execute_query("SELECT full_name, email FROM Users WHERE user_id=%s", (session['user_id'],), fetchone=True)
    return render_template('alumni/edit_profile.html', profile=profile, departments=departments, user=user or {'full_name': 'Alice Johnson', 'email': 'alice@example.com'})

# ─────────────────────────────────────────────
# JOBS
# ─────────────────────────────────────────────
@alumni_bp.route('/jobs')
@alumni_required
def my_jobs():
    profile = get_alumni_profile(session['user_id'])
    alumni_id = profile['alumni_id'] if profile else 1
    jobs = execute_query("SELECT * FROM Job WHERE alumni_id=%s ORDER BY created_at DESC", (alumni_id,), fetch=True) or []
    return render_template('alumni/my_jobs.html', jobs=jobs)


@alumni_bp.route('/jobs/add', methods=['GET', 'POST'])
@alumni_required
def add_job():
    profile = get_alumni_profile(session['user_id'])
    alumni_id = profile['alumni_id'] if profile else 1

    if request.method == 'POST':
        company  = request.form.get('company_name', '').strip()
        title    = request.form.get('job_title', '').strip()
        desc     = request.form.get('job_description', '').strip()
        job_type = request.form.get('job_type', 'Internship')
        link     = request.form.get('application_link', '').strip()
        location = request.form.get('location', '').strip()
        deadline = request.form.get('deadline') or None

        execute_query("""
            INSERT INTO Job (alumni_id, company_name, job_title, job_description,
                             job_type, application_link, location, deadline)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (alumni_id, company, title, desc, job_type, link, location, deadline))

        flash('Job posted successfully!', 'success')
        return redirect(url_for('alumni.my_jobs'))

    return render_template('alumni/add_job.html')


@alumni_bp.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
@alumni_required
def edit_job(job_id):
    job = execute_query("SELECT * FROM Job WHERE job_id=%s", (job_id,), fetchone=True)
    if not job:
        flash('Job not found.', 'danger')
        return redirect(url_for('alumni.my_jobs'))

    if request.method == 'POST':
        company  = request.form.get('company_name', '').strip()
        title    = request.form.get('job_title', '').strip()
        desc     = request.form.get('job_description', '').strip()
        job_type = request.form.get('job_type', '')
        link     = request.form.get('application_link', '').strip()
        location = request.form.get('location', '').strip()
        deadline = request.form.get('deadline') or None

        execute_query("""
            UPDATE Job SET company_name=%s, job_title=%s, job_description=%s,
                           job_type=%s, application_link=%s, location=%s, deadline=%s
            WHERE job_id=%s
        """, (company, title, desc, job_type, link, location, deadline, job_id))
        flash('Job updated.', 'success')
        return redirect(url_for('alumni.my_jobs'))

    return render_template('alumni/edit_job.html', job=job)


@alumni_bp.route('/jobs/delete/<int:job_id>', methods=['POST'])
@alumni_required
def delete_job(job_id):
    execute_query("DELETE FROM Job WHERE job_id=%s", (job_id,))
    flash('Job deleted.', 'success')
    return redirect(url_for('alumni.my_jobs'))


# ─────────────────────────────────────────────
# MENTORSHIP REQUESTS
# ─────────────────────────────────────────────
@alumni_bp.route('/mentorship')
@alumni_required
def mentorship_requests():
    profile = get_alumni_profile(session['user_id'])
    alumni_id = profile['alumni_id'] if profile else 1

    requests_list = execute_query("""
        SELECT m.mentorship_id, m.message, m.request_status, m.requested_at,
               u.full_name AS student_name, u.email AS student_email,
               d.department_name, s.current_year, s.skills AS student_skills
        FROM Mentorship m
        JOIN Student s ON m.student_id = s.student_id
        JOIN Users u ON s.user_id = u.user_id
        JOIN Department d ON s.department_id = d.department_id
        WHERE m.alumni_id=%s
        ORDER BY m.requested_at DESC
    """, (alumni_id,), fetch=True) or []
    return render_template('alumni/mentorship.html', requests=requests_list)


@alumni_bp.route('/mentorship/update/<int:mentorship_id>', methods=['POST'])
@alumni_required
def update_mentorship(mentorship_id):
    status = request.form.get('status', 'Accepted')
    execute_query("UPDATE Mentorship SET request_status=%s WHERE mentorship_id=%s", (status, mentorship_id))
    flash(f'Mentorship request {status.lower()} successfully!', 'success')
    return redirect(url_for('alumni.mentorship_requests'))
