#!/usr/bin/env python3
"""
Diagnostic script to check your setup and tell you exactly what is missing.
Run with: python3 check_setup.py
"""

import sys
import os

print("\n" + "="*50)
print("🔍 ALUMNI MANAGEMENT SYSTEM - DIAGNOSTIC CHECK")
print("="*50 + "\n")

# 1. Python Check
print(f"1. Python Version: {sys.version.split()[0]} ... ✅ OK")

# 2. Package Check
packages = {
    'flask': 'Flask',
    'mysql.connector': 'mysql-connector-python',
    'dotenv': 'python-dotenv',
    'werkzeug': 'Werkzeug'
}

missing_packages = []
for module_name, pip_name in packages.items():
    try:
        __import__(module_name)
        print(f"2. Package '{pip_name}' ... ✅ INSTALLED")
    except ImportError:
        print(f"2. Package '{pip_name}' ... ❌ MISSING")
        missing_packages.append(pip_name)

if missing_packages:
    print("\n👉 TO FIX MISSING PACKAGES, RUN THIS:")
    print("   pip install " + " ".join(missing_packages))
    print("   (or: pip install --break-system-packages " + " ".join(missing_packages) + ")\n")

# 3. .env File Check
if os.path.exists('.env'):
    print("3. Configuration file (.env) ... ✅ EXISTS")
else:
    print("3. Configuration file (.env) ... ❌ MISSING (run: cp .env.example .env)")

# 4. MySQL Server Connection Check
try:
    from config import Config
    import mysql.connector

    print(f"\n4. Testing connection to MySQL at {Config.DB_HOST}:{Config.DB_PORT} as user '{Config.DB_USER}'...")
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            connection_timeout=3
        )
        print("   Connection to MySQL Server ... ✅ SUCCESSFUL!")
        
        # Check if database exists
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES LIKE %s", (Config.DB_NAME,))
        db_exists = cursor.fetchone()
        
        if db_exists:
            print(f"5. Database '{Config.DB_NAME}' ... ✅ EXISTS")
            cursor.execute(f"USE {Config.DB_NAME};")
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            print(f"6. Tables found ({len(tables)} tables) ... ✅ OK")
            if len(tables) == 0:
                print("   👉 Database is empty. Run: python3 init_db.py")
        else:
            print(f"5. Database '{Config.DB_NAME}' ... ❌ NOT FOUND")
            print("   👉 Run: python3 init_db.py to create it automatically!")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"   Connection to MySQL Server ... ❌ FAILED: {err}")
        print("\n👉 HOW TO FIX MYSQL:")
        print("   a) Make sure MySQL is running: sudo systemctl start mysql")
        print("   b) If password was set, update DB_PASSWORD in .env file")

except Exception as e:
    print(f"   Could not test MySQL: {e}")

print("\n" + "="*50 + "\n")
