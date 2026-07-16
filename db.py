import sqlite3

def connect_db():
    return sqlite3.connect("database.db", check_same_thread=False)

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            name TEXT,
            ats_score INTEGER,
            status TEXT,
            matching_skills TEXT,
            missing_skills TEXT,
            reason TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_resume(data):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO resumes 
        (role, name, ats_score, status, matching_skills, missing_skills, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def get_by_role_and_status(role, status):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, ats_score, matching_skills, missing_skills, reason 
        FROM resumes WHERE role=? AND status=?
    """, (role, status))
    rows = cur.fetchall()
    conn.close()
    return rows
