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
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL,
    instructor TEXT NOT NULL,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS assignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    title TEXT NOT NULL,
    due_date TEXT,
    points_possible INTEGER,
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS announcements (
    announcement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    post_date TEXT,
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER,
    student_id INTEGER,
    score REAL,
    comments TEXT,
    FOREIGN KEY(assignment_id) REFERENCES assignments(assignment_id),
    FOREIGN KEY(student_id) REFERENCES users(user_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER,
    student_id INTEGER,
    comments TEXT,
    post_date TEXT,
    FOREIGN KEY(assignment_id) REFERENCES assignments(assignment_id),
    FOREIGN KEY(student_id) REFERENCES users(user_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS lesson_plans (
    lesson_plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    upload_date TEXT,
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS learning_objectives (
    objective_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    description TEXT NOT NULL,
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assignment_id INTEGER,
    student_id INTEGER,
    submission_text TEXT NOT NULL,
    submission_date TEXT,
    status TEXT,
    FOREIGN KEY(assignment_id) REFERENCES assignments(assignment_id),
    FOREIGN KEY(student_id) REFERENCES users(user_id)
)
""")

cursor.execute("""
INSERT OR IGNORE INTO users (user_id, name, email, password, role)
VALUES
(1, 'Student User', 'student@test.com', 'password', 'Student'),
(2, 'Instructor User', 'instructor@test.com', 'password', 'Instructor'),
(3, 'Admin User', 'admin@test.com', 'password', 'Administrator')
""")

cursor.execute("""
INSERT OR IGNORE INTO courses (course_id, course_name, instructor, description)
VALUES
(1, 'COM-430 Software Engineering', 'Instructor User', 'Software engineering and DevOps project course')
""")

cursor.execute("""
INSERT OR IGNORE INTO assignments (assignment_id, course_id, title, due_date, points_possible)
VALUES
(1, 1, 'DevOps Submission 3 - Topology Report', '2026-06-07', 100)
""")

cursor.execute("""
INSERT OR IGNORE INTO announcements (announcement_id, course_id, title, message, post_date)
VALUES
(1, 1, 'Module 6 Update', 'The project is being refined for role separation, testing, and code organization.', '2026-06-12')
""")

cursor.execute("""
INSERT OR IGNORE INTO grades (grade_id, assignment_id, student_id, score, comments)
VALUES
(1, 1, 1, 95, 'Strong progress on Flask, SQLite, GitHub, and Jenkins setup.')
""")

cursor.execute("""
INSERT OR IGNORE INTO feedback (feedback_id, assignment_id, student_id, comments, post_date)
VALUES
(1, 1, 1, 'Good work establishing the initial DevOps pipeline and application shell.', '2026-06-05')
""")

cursor.execute("""
INSERT OR IGNORE INTO lesson_plans (lesson_plan_id, course_id, title, content, upload_date)
VALUES
(1, 1, 'Module 6 Role Separation Lesson Plan', 'Review role-based access, admin responsibilities, instructor responsibilities, and test-stage promotion.', '2026-06-12')
""")

cursor.execute("""
INSERT OR IGNORE INTO learning_objectives (objective_id, course_id, description)
VALUES
(1, 1, 'Demonstrate role-based system design using student, instructor, and administrator dashboards.')
""")

cursor.execute("""
INSERT OR IGNORE INTO submissions (submission_id, assignment_id, student_id, submission_text, submission_date, status)
VALUES
(1, 1, 1, 'Initial topology report submitted for review.', '2026-06-05', 'Submitted')
""")

conn.commit()
conn.close()

print("Database initialized successfully.")