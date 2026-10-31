
import sqlite3
import bcrypt

# Create database
def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Register user
def register_user(username, password):

    if not username or not password:
        return False, "Please enter username and password."

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    if cursor.fetchone():
        conn.close()
        return False, "Username already exists."

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password.decode("utf-8"))
    )

    conn.commit()
    conn.close()

    return True, "Registration successful!"


# Login user
def login_user(username, password):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return False

    stored_password = result[0].encode("utf-8")

    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password
    )


# Initialize database
create_database()
