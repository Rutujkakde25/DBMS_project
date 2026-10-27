from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.db_connection import execute_query, execute_transaction
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

auth_bp = Blueprint('auth', __name__)

# ─────────────────────────────────────────────
# ONE-CLICK INSTANT DEMO LOGIN (NO PASSWORDS NEEDED!)
# ─────────────────────────────────────────────
@auth_bp.route('/demo/<role>')
def demo_login(role):
    if role == 'admin':
        session['user_id'] = 1
        session['full_name'] = 'System Administrator (Demo)'
        session['email'] = 'admin@alumni.example.com'
        session['role'] = 'admin'
        flash('⚡ Switched to Admin Mode! You have full access.', 'success')
        return redirect(url_for('admin.dashboard'))
    elif role == 'alumni':
        session['user_id'] = 2
        session['full_name'] = 'Alice Johnson (Demo Alumni)'
        session['email'] = 'alice.johnson@example.com'
        session['role'] = 'alumni'
        flash('⚡ Switched to Alumni Mode! (Alice Johnson - Google LLC)', 'success')
        return redirect(url_for('alumni.dashboard'))
    elif role == 'student':
        session['user_id'] = 10
        session['full_name'] = 'Kate Brown (Demo Student)'
        session['email'] = 'kate.brown@example.com'
        session['role'] = 'student'
        flash('⚡ Switched to Student Mode! (Kate Brown - 3rd Year CSE)', 'success')
        return redirect(url_for('student.dashboard'))
    return redirect(url_for('index'))


# ─────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email     = request.form.get('email', '').strip().lower()
        password  = request.form.get('password', '123456')
        role      = request.form.get('role', 'student')

        if not full_name or not email:
            flash('Name and Email are required.', 'danger')
            return redirect(url_for('auth.register'))

        existing = execute_query("SELECT user_id FROM Users WHERE email=%s", (email,), fetchone=True)
        if existing:
            flash('This email is already registered.', 'warning')
            return redirect(url_for('auth.login'))

        password_hash = generate_password_hash(password)
        status = 'approved' # Auto-approve for smooth demo!

        from database.db_connection import get_db_connection
        conn = get_db_connection()
        try:
            # Insert User
            new_user_id = execute_query(
                "INSERT INTO Users (full_name, email, password_hash, role, account_status) VALUES (%s,%s,%s,%s,%s)",
                (full_name, email, password_hash, role, status), lastrowid=True
            )

            dept_id = request.form.get('department_id', 1)

            if role == 'alumni':
                grad_year = request.form.get('graduation_year', 2024)
                company = request.form.get('current_company', 'Tech Corp')
                title = request.form.get('job_title', 'Software Engineer')
                execute_query(
                    "INSERT INTO Alumni (user_id, department_id, graduation_year, current_company, job_title) VALUES (%s,%s,%s,%s,%s)",
                    (new_user_id, dept_id, grad_year, company, title)
                )
            else:
                curr_year = request.form.get('current_year', 3)
                execute_query(
                    "INSERT INTO Student (user_id, department_id, current_year) VALUES (%s,%s,%s)",
                    (new_user_id, dept_id, curr_year)
                )

            # Automatically log the new user in for demo!
            session['user_id'] = new_user_id
            session['full_name'] = full_name
            session['email'] = email
            session['role'] = role

            flash(f'Account created! Logged in as {full_name}.', 'success')
            return redirect(url_for('auth.dashboard_redirect'))

        except Exception as e:
            flash(f'Registration error: {e}', 'danger')
            return redirect(url_for('auth.register'))

    departments = execute_query("SELECT * FROM Department ORDER BY department_name", fetch=True) or []
    return render_template('register.html', departments=departments)


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = execute_query(
            "SELECT user_id, full_name, email, password_hash, role, account_status FROM Users WHERE email=%s",
            (email,), fetchone=True
        )

        if user:
            # Relaxed for demo: allow login
            session['user_id']   = user['user_id']
            session['full_name'] = user['full_name']
            session['email']     = user['email']
            session['role']      = user['role']
            session.permanent    = True

            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('auth.dashboard_redirect'))
        else:
            flash('User not found. Use the 1-Click Demo buttons below!', 'warning')

    return render_template('login.html')


# ─────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('index'))


# ─────────────────────────────────────────────
# DASHBOARD REDIRECT
# ─────────────────────────────────────────────
@auth_bp.route('/dashboard')
def dashboard_redirect():
    role = session.get('role', 'admin')
    if role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif role == 'alumni':
        return redirect(url_for('alumni.dashboard'))
    elif role == 'student':
        return redirect(url_for('student.dashboard'))
    return redirect(url_for('index'))
