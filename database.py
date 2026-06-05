import sqlite3
import os

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/course_app.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cursor.execute("""
INSERT OR IGNORE INTO users (user_id, name, email, password, role)
VALUES
(1, 'Student User', 'student@test.com', 'password', 'Student'),
(2, 'Instructor User', 'instructor@test.com', 'password', 'Instructor'),
(3, 'Admin User', 'admin@test.com', 'password', 'Administrator')
""")

conn.commit()
conn.close()

print("Database initialized successfully.")