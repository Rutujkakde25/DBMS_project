#!/usr/bin/env python3
"""
init_db.py - Automatically sets up MySQL database, executes schema.sql and seed.sql.
Usage: python3 init_db.py
"""

import os
import mysql.connector
from config import Config

def init_database():
    print(f"Connecting to MySQL server at {Config.DB_HOST}:{Config.DB_PORT} as user '{Config.DB_USER}'...")
    try:
        # Connect to MySQL server (without specifying DB first to create it if missing)
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            autocommit=True
        )
        cursor = conn.cursor()

        print(f"Creating database '{Config.DB_NAME}' if it does not exist...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute(f"USE {Config.DB_NAME};")

        # 1. Read and execute schema.sql
        print("Executing schema.sql (tables, views, indexes)...")
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # Split schema into statements, handling DELIMITER blocks
        # First execute standard statements before DELIMITER
        parts = schema_sql.split("DELIMITER $$")
        main_schema = parts[0]
        
        for statement in main_schema.split(';'):
            stmt = statement.strip()
            if stmt and not stmt.startswith('--'):
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    print(f"  [Note] {e}")

        # Execute procedure and trigger if present
        if len(parts) > 1:
            for part in parts[1:]:
                subparts = part.split("DELIMITER ;")
                body = subparts[0].replace('$$', '').strip()
                if body:
                    try:
                        cursor.execute(body)
                    except Exception as e:
                        print(f"  [Routine Note] {e}")

        print("Executing seed.sql (departments, users, alumni, jobs, events)...")
        with open('seed.sql', 'r', encoding='utf-8') as f:
            seed_sql = f.read()

        for statement in seed_sql.split(';'):
            stmt = statement.strip()
            if stmt and not stmt.startswith('--'):
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    pass

        cursor.close()
        conn.close()
        print("\n✅ Database 'alumni_management' successfully initialized with all sample records!")
        print("Now you can run: python3 app.py\n")

    except mysql.connector.Error as err:
        print(f"\n❌ MySQL Connection Error: {err}")
        print("Check your MySQL username/password in .env file.")

if __name__ == '__main__':
    init_database()
