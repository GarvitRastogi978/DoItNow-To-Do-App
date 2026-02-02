import sqlite3
import hashlib
from datetime import datetime


DB_NAME = "todo.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    user = cursor.fetchone()
    conn.close()
    return user


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            priority TEXT,
            status TEXT,
            due_date TEXT,
            time_spent INTEGER DEFAULT 0,
            timer_start TEXT
        )
    """)
    conn.commit()
    conn.close()



def add_task(user_id, title, priority, due_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (user_id, title, priority, status, due_date) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, priority, "Pending", due_date)
    )
    conn.commit()
    conn.close()



def get_tasks(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tasks WHERE user_id = ?", (user_id,)
    )
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_status(task_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Add Time Tracking Functions
def start_timer(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET timer_start=? WHERE id=?",
        (datetime.now().isoformat(), task_id)
    )
    conn.commit()
    conn.close()

def stop_timer(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT timer_start, time_spent FROM tasks WHERE id=?",
        (task_id,)
    )
    start_time, total_time = cursor.fetchone()

    if start_time:
        start = datetime.fromisoformat(start_time)
        elapsed = int((datetime.now() - start).total_seconds())
        total_time += elapsed

        cursor.execute(
            "UPDATE tasks SET time_spent=?, timer_start=NULL WHERE id=?",
            (total_time, task_id)
        )

    conn.commit()
    conn.close()
