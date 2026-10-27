from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from database.db_connection import execute_query, execute_transaction
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ─────────────────────────────────────────────
# DECORATOR: Demo-friendly (auto-logs in as Admin if not logged in)
# ─────────────────────────────────────────────
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            # Auto-assign Admin session for seamless live demo!
            session['user_id'] = 1
            session['full_name'] = 'System Administrator (Demo)'
            session['role'] = 'admin'
            session['email'] = 'admin@alumni.example.com'
        return f(*args, **kwargs)
    return decorated


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {}

    row = execute_query("SELECT COUNT(*) AS cnt FROM Alumni a JOIN Users u ON a.user_id=u.user_id WHERE u.account_status='approved'", fetchone=True)
    stats['total_alumni'] = row['cnt'] if row else 0

    row = execute_query("SELECT COUNT(*) AS cnt FROM Student", fetchone=True)
    stats['total_students'] = row['cnt'] if row else 0

    row = execute_query("SELECT COUNT(*) AS cnt FROM Job", fetchone=True)
    stats['total_jobs'] = row['cnt'] if row else 0

    row = execute_query("SELECT COUNT(*) AS cnt FROM Users WHERE account_status='pending' AND role='alumni'", fetchone=True)
    stats['pending_approvals'] = row['cnt'] if row else 0

    row = execute_query("SELECT COUNT(*) AS cnt FROM Event", fetchone=True)
    stats['total_events'] = row['cnt'] if row else 0

    row = execute_query("SELECT COUNT(*) AS cnt FROM Mentorship", fetchone=True)
    stats['total_mentorships'] = row['cnt'] if row else 0

    dept_stats = execute_query("""
        SELECT d.department_name, COUNT(a.alumni_id) AS alumni_count
        FROM Department d
        LEFT JOIN Alumni a ON d.department_id = a.department_id
        GROUP BY d.department_id, d.department_name
        ORDER BY alumni_count DESC
    """, fetch=True) or []

    mentorship_stats = execute_query("""
        SELECT request_status, COUNT(*) AS cnt
        FROM Mentorship
        GROUP BY request_status
    """, fetch=True) or []

    pending = execute_query("""
        SELECT u.user_id, u.full_name, u.email, u.created_at,
               d.department_name, a.graduation_year
        FROM Users u
        JOIN Alumni a ON u.user_id = a.user_id
        JOIN Department d ON a.department_id = d.department_id
        WHERE u.account_status = 'pending'
        ORDER BY u.created_at DESC LIMIT 5
    """, fetch=True) or []

    return render_template('admin/dashboard.html',
                           stats=stats,
                           dept_stats=dept_stats,
                           mentorship_stats=mentorship_stats,
                           pending=pending)


# ─────────────────────────────────────────────
# MANAGE ALUMNI
# ─────────────────────────────────────────────
@admin_bp.route('/alumni')
@admin_required
def manage_alumni():
    alumni = execute_query("""
        SELECT u.user_id, u.full_name, u.email, u.account_status, u.created_at,
               d.department_name, a.graduation_year, a.current_company, a.job_title, a.alumni_id
        FROM Users u
        JOIN Alumni a ON u.user_id = a.user_id
        JOIN Department d ON a.department_id = d.department_id
        ORDER BY u.created_at DESC
    """, fetch=True) or []
    return render_template('admin/manage_alumni.html', alumni=alumni)


@admin_bp.route('/alumni/approve/<int:user_id>', methods=['POST'])
@admin_required
def approve_alumni(user_id):
    execute_query("UPDATE Users SET account_status='approved' WHERE user_id=%s", (user_id,))
    flash('Alumni approved successfully.', 'success')
    return redirect(url_for('admin.manage_alumni'))


@admin_bp.route('/alumni/reject/<int:user_id>', methods=['POST'])
@admin_required
def reject_alumni(user_id):
    execute_query("UPDATE Users SET account_status='rejected' WHERE user_id=%s", (user_id,))
    flash('Alumni registration rejected.', 'warning')
    return redirect(url_for('admin.manage_alumni'))


@admin_bp.route('/alumni/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_alumni(user_id):
    execute_query("DELETE FROM Users WHERE user_id=%s", (user_id,))
    flash('Alumni record deleted.', 'success')
    return redirect(url_for('admin.manage_alumni'))


# ─────────────────────────────────────────────
# MANAGE STUDENTS
# ─────────────────────────────────────────────
@admin_bp.route('/students')
@admin_required
def manage_students():
    students = execute_query("""
        SELECT u.user_id, u.full_name, u.email, u.account_status, u.created_at,
               d.department_name, s.current_year, s.student_id
        FROM Users u
        JOIN Student s ON u.user_id = s.user_id
        JOIN Department d ON s.department_id = d.department_id
        ORDER BY u.created_at DESC
    """, fetch=True) or []
    return render_template('admin/manage_students.html', students=students)


@admin_bp.route('/students/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_student(user_id):
    execute_query("DELETE FROM Users WHERE user_id=%s", (user_id,))
    flash('Student record deleted.', 'success')
    return redirect(url_for('admin.manage_students'))


# ─────────────────────────────────────────────
# MANAGE DEPARTMENTS
# ─────────────────────────────────────────────
@admin_bp.route('/departments')
@admin_required
def manage_departments():
    departments = execute_query("""
        SELECT d.department_id, d.department_name,
               COUNT(DISTINCT a.alumni_id) AS alumni_count,
               COUNT(DISTINCT s.student_id) AS student_count
        FROM Department d
        LEFT JOIN Alumni a ON d.department_id = a.department_id
        LEFT JOIN Student s ON d.department_id = s.department_id
        GROUP BY d.department_id, d.department_name
        ORDER BY d.department_name
    """, fetch=True) or []
    return render_template('admin/manage_departments.html', departments=departments)


@admin_bp.route('/departments/add', methods=['POST'])
@admin_required
def add_department():
    name = request.form.get('department_name', '').strip()
    if name:
        execute_query("INSERT INTO Department (department_name) VALUES (%s)", (name,))
        flash(f'Department "{name}" added successfully.', 'success')
    return redirect(url_for('admin.manage_departments'))


@admin_bp.route('/departments/delete/<int:dept_id>', methods=['POST'])
@admin_required
def delete_department(dept_id):
    execute_query("DELETE FROM Department WHERE department_id=%s", (dept_id,))
    flash('Department deleted.', 'success')
    return redirect(url_for('admin.manage_departments'))


# ─────────────────────────────────────────────
# MANAGE EVENTS
# ─────────────────────────────────────────────
@admin_bp.route('/events')
@admin_required
def manage_events():
    events = execute_query("""
        SELECT e.event_id, e.event_name, e.description, e.event_date, e.venue,
               u.full_name AS created_by_name,
               COUNT(er.registration_id) AS reg_count
        FROM Event e
        JOIN Users u ON e.created_by = u.user_id
        LEFT JOIN Event_Registration er ON e.event_id = er.event_id
        GROUP BY e.event_id
        ORDER BY e.event_date DESC
    """, fetch=True) or []
    return render_template('admin/manage_events.html', events=events)


@admin_bp.route('/events/add', methods=['POST'])
@admin_required
def add_event():
    name  = request.form.get('event_name', '').strip()
    desc  = request.form.get('description', '').strip()
    date  = request.form.get('event_date', '')
    venue = request.form.get('venue', '').strip()

    if name and date:
        execute_query(
            "INSERT INTO Event (event_name, description, event_date, venue, created_by) VALUES (%s,%s,%s,%s,%s)",
            (name, desc, date, venue, session.get('user_id', 1))
        )
        flash(f'Event "{name}" created.', 'success')
    return redirect(url_for('admin.manage_events'))


@admin_bp.route('/events/delete/<int:event_id>', methods=['POST'])
@admin_required
def delete_event(event_id):
    execute_query("DELETE FROM Event WHERE event_id=%s", (event_id,))
    flash('Event deleted.', 'success')
    return redirect(url_for('admin.manage_events'))


# ─────────────────────────────────────────────
# REPORTS
# ─────────────────────────────────────────────
@admin_bp.route('/reports')
@admin_required
def reports():
    by_year = execute_query("""
        SELECT a.graduation_year, COUNT(*) AS cnt
        FROM Alumni a JOIN Users u ON a.user_id=u.user_id
        GROUP BY a.graduation_year ORDER BY a.graduation_year
    """, fetch=True) or []

    by_company = execute_query("""
        SELECT company_name, COUNT(*) AS cnt
        FROM Job GROUP BY company_name ORDER BY cnt DESC LIMIT 10
    """, fetch=True) or []

    above_avg = execute_query("""
        SELECT d.department_name, COUNT(a.alumni_id) AS cnt
        FROM Department d
        JOIN Alumni a ON d.department_id = a.department_id
        GROUP BY d.department_id, d.department_name
        ORDER BY cnt DESC
    """, fetch=True) or []

    no_request = execute_query("""
        SELECT u.full_name, u.email, d.department_name
        FROM Student s
        LEFT JOIN Mentorship m ON s.student_id = m.student_id
        JOIN Users u ON s.user_id = u.user_id
        JOIN Department d ON s.department_id = d.department_id
        WHERE m.mentorship_id IS NULL
    """, fetch=True) or []

    event_reg = execute_query("""
        SELECT e.event_name, COUNT(er.registration_id) AS reg_count
        FROM Event e
        LEFT JOIN Event_Registration er ON e.event_id = er.event_id
        GROUP BY e.event_id, e.event_name ORDER BY reg_count DESC
    """, fetch=True) or []

    return render_template('admin/reports.html',
                           by_year=by_year,
                           by_company=by_company,
                           above_avg=above_avg,
                           no_request=no_request,
                           event_reg=event_reg)
