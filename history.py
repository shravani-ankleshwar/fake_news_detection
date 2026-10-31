
import sqlite3
from datetime import datetime


# Create history database
def create_history_table():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            news TEXT,
            prediction TEXT,
            confidence REAL,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()


# Save prediction history
def save_history(username, news, prediction, confidence):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO history
        (username, news, prediction, confidence, date)
        VALUES (?, ?, ?, ?, ?)
    """, (username, news, prediction, confidence, date))

    conn.commit()
    conn.close()


# Get user's history
def get_history(username):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT news, prediction, confidence, date
        FROM history
        WHERE username = ?
        ORDER BY id DESC
    """, (username,))

    records = cursor.fetchall()

    conn.close()

    return records


# Initialize history database
create_history_table()
