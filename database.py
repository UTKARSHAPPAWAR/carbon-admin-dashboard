import sqlite3
import hashlib

def get_connection():
    return sqlite3.connect("users.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Users table with role and email
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, role TEXT, email TEXT)''')
    
    # Migration: add role/email columns if they don't exist
    try:
        c.execute("ALTER TABLE users ADD COLUMN role TEXT")
    except sqlite3.OperationalError:
        pass 
    try:
        c.execute("ALTER TABLE users ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    
    # Projects table
    c.execute('''CREATE TABLE IF NOT EXISTS projects
                 (id TEXT PRIMARY KEY, name TEXT, type TEXT, location TEXT, 
                  credits REAL, description TEXT, status TEXT, developer TEXT,
                  issued REAL, retired REAL)''')
    
    # Purchases table
    c.execute('''CREATE TABLE IF NOT EXISTS purchases
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, project_id TEXT, 
                  amount REAL, date TEXT)''')
    
    # Activity Log table
    c.execute('''CREATE TABLE IF NOT EXISTS activity_log
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, activity_type TEXT, 
                  description TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    
    # Add default admin (Password: 123456)
    admin_pass = hashlib.sha256("123456".encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", admin_pass, "admin"))
        conn.commit()
    except sqlite3.IntegrityError:
        # Update existing admin to new password and ensure role is set
        c.execute("UPDATE users SET password = ?, role = ? WHERE username = ?", (admin_pass, "admin", "admin"))
        conn.commit()

    # Add sample projects if empty
    c.execute("SELECT COUNT(*) FROM projects")
    if c.fetchone()[0] == 0:
        sample_projects = [
            ("VCS-001", "Amazon Rainforest Conservation", "Nature-based/REDD+", "Brazil", 500000.0, "Protecting biodiversity in the Amazon.", "Verified", "BioClean Solutions", 500000.0, 120000.0),
            ("GS-442", "Community Wind Power India", "Renewable Energy", "India", 250000.0, "Wind turbines for rural electrification.", "Verified", "GreenPath Energy", 250000.0, 210000.0),
            ("REG-SAMPLE", "Example Pending Project", "Waste Management", "Kenya", 1500.0, "A sample project for verification test.", "Pending", "User Registered", 1500.0, 0.0)
        ]
        c.executemany("INSERT INTO projects VALUES (?,?,?,?,?,?,?,?,?,?)", sample_projects)
        conn.commit()
    conn.close()

def add_user(username, hashed_password, role="user", email=None):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)", (username, hashed_password, role, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def log_activity(username, activity_type, description):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO activity_log (username, activity_type, description) VALUES (?, ?, ?)", 
              (username, activity_type, description))
    conn.commit()
    conn.close()

def get_all_activity_logs():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT username, activity_type, description, timestamp FROM activity_log ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return data

def get_activity_log(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT activity_type, description, timestamp FROM activity_log WHERE username = ? ORDER BY timestamp DESC", (username,))
    data = c.fetchall()
    conn.close()
    return data

def update_user_email(username, email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET email = ? WHERE username = ?", (email, username))
    conn.commit()
    conn.close()

def get_user_email(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE username = ?", (username,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else None

def verify_user(username, hashed_password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def get_projects(status=None):
    conn = get_connection()
    c = conn.cursor()
    if status:
        c.execute("SELECT * FROM projects WHERE status = ?", (status,))
    else:
        c.execute("SELECT * FROM projects")
    cols = [d[0] for d in c.description]
    data = [dict(zip(cols, row)) for row in c.fetchall()]
    conn.close()
    return data

def update_project_status(p_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE projects SET status = ? WHERE id = ?", (status, p_id))
    conn.commit()
    conn.close()

def add_project(proj):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO projects VALUES (?,?,?,?,?,?,?,?,?,?)''', 
              (proj['ID'], proj['Project Name'], proj['Type'], proj['Location'], 
               proj['Issued'], proj['Description'], proj['Status'], proj['Developer'],
               proj['Issued'], proj['Retired']))
    conn.commit()
    conn.close()

def get_purchases():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM purchases")
    cols = [d[0] for d in c.description]
    data = [dict(zip(cols, row)) for row in c.fetchall()]
    conn.close()
    return data

def add_purchase(username, project_id, amount):
    conn = get_connection()
    c = conn.cursor()
    from datetime import datetime
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO purchases (username, project_id, amount, date) VALUES (?, ?, ?, ?)", 
              (username, project_id, amount, now_str))
    conn.commit()
    conn.close()
