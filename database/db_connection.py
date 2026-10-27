import os
import sqlite3
from config import Config

# Path for SQLite database fallback
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'alumni_management.sqlite3')

USE_SQLITE = False

def get_mysql_connection():
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            charset='utf8mb4',
            connection_timeout=2
        )
        return conn
    except Exception as e:
        return None

def get_sqlite_connection():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys in SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def get_db_connection():
    """Returns MySQL connection if available, otherwise seamlessly falls back to pre-seeded SQLite."""
    global USE_SQLITE
    if not USE_SQLITE:
        mysql_conn = get_mysql_connection()
        if mysql_conn:
            return mysql_conn
        else:
            # Fallback to SQLite
            USE_SQLITE = True
            print("[INFO] MySQL not reachable, using self-contained local database (SQLite fallback).")
    
    return get_sqlite_connection()

def execute_query(query, params=None, fetch=False, fetchone=False, lastrowid=False):
    """
    Execute a parameterized SQL query safely.
    Works for both MySQL and SQLite seamlessly.
    """
    global USE_SQLITE
    conn = get_db_connection()
    if conn is None:
        return None

    is_sqlite = isinstance(conn, sqlite3.Connection)
    cursor = None
    try:
        if is_sqlite:
            # Convert MySQL %s placeholders to SQLite ? placeholders if needed
            converted_query = query.replace('%s', '?')
            # Handle CURDATE() in SQLite
            converted_query = converted_query.replace('CURDATE()', "date('now')")
            cursor = conn.cursor()
            cursor.execute(converted_query, params or ())
            
            if fetchone:
                row = cursor.fetchone()
                return dict(row) if row else None
            elif fetch:
                rows = cursor.fetchall()
                return [dict(r) for r in rows] if rows else []
            elif lastrowid:
                conn.commit()
                return cursor.lastrowid
            else:
                conn.commit()
                return cursor.rowcount
        else:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())

            if fetchone:
                return cursor.fetchone()
            elif fetch:
                return cursor.fetchall() or []
            elif lastrowid:
                conn.commit()
                return cursor.lastrowid
            else:
                conn.commit()
                return cursor.rowcount

    except Exception as e:
        print(f"[QUERY ERROR] {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        if conn:
            conn.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute_transaction(queries_and_params):
    """Execute multiple queries inside an atomic transaction."""
    conn = get_db_connection()
    if conn is None:
        return False
    is_sqlite = isinstance(conn, sqlite3.Connection)
    cursor = None
    try:
        if is_sqlite:
            cursor = conn.cursor()
            results = []
            for query, params in queries_and_params:
                q = query.replace('%s', '?')
                cursor.execute(q, params or ())
                results.append(cursor.lastrowid)
            conn.commit()
            return results
        else:
            cursor = conn.cursor(dictionary=True)
            conn.start_transaction()
            results = []
            for query, params in queries_and_params:
                cursor.execute(query, params or ())
                results.append(cursor.lastrowid)
            conn.commit()
            return results
    except Exception as e:
        print(f"[TRANSACTION ERROR] {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
