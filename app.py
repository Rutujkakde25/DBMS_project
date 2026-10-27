from flask import Flask, render_template, redirect, url_for, session
from config import Config
import os

# Auto-ensure pre-populated database exists so departments & records are NEVER empty
try:
    from setup_local_db import populate_database
    populate_database()
except Exception as e:
    print(f"[STARTUP NOTE] {e}")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # Register Blueprints
    from routes.auth    import auth_bp
    from routes.admin   import admin_bp
    from routes.alumni  import alumni_bp
    from routes.student import student_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(alumni_bp)
    app.register_blueprint(student_bp)

    # ─── Public Routes ───────────────────────────────────
    @app.route('/')
    def index():
        from database.db_connection import execute_query
        stats = {}
        r = execute_query("SELECT COUNT(*) AS cnt FROM Alumni a JOIN Users u ON a.user_id=u.user_id WHERE u.account_status='approved'", fetchone=True)
        stats['alumni'] = r['cnt'] if r else 0
        r = execute_query("SELECT COUNT(*) AS cnt FROM Job", fetchone=True)
        stats['jobs'] = r['cnt'] if r else 0
        r = execute_query("SELECT COUNT(*) AS cnt FROM Department", fetchone=True)
        stats['departments'] = r['cnt'] if r else 0
        r = execute_query("SELECT COUNT(*) AS cnt FROM Event", fetchone=True)
        stats['events'] = r['cnt'] if r else 0
        return render_template('index.html', stats=stats)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/directory')
    def directory():
        from database.db_connection import execute_query
        alumni = execute_query("""
            SELECT full_name, department_name, graduation_year,
                   current_company, job_title, skills, linkedin_url
            FROM alumni_directory_view
            ORDER BY graduation_year DESC, full_name ASC
            LIMIT 20
        """, fetch=True) or []
        departments = execute_query("SELECT * FROM Department ORDER BY department_name", fetch=True) or []
        return render_template('directory.html', alumni=alumni, departments=departments)

    # ─── Error Handlers ───────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    return app


if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*55)
    print("🎓 ALUMNI NETWORKING MANAGEMENT SYSTEM IS RUNNING!")
    print("👉 Open your browser at: http://localhost:5000")
    print("="*55 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
