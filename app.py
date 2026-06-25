from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import date
import calendar as py_calendar

app = Flask(__name__)
app.secret_key = "dev_secret_key"

DATABASE = "database/course_app.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def login_required():
    return "user_id" in session


def role_required(*allowed_roles):
    return "user_id" in session and session["role"] in allowed_roles


def student_required():
    return role_required("Student")


def instructor_required():
    return role_required("Instructor")


def admin_required():
    return role_required("Administrator")


def admin_or_instructor_required():
    return role_required("Instructor", "Administrator")


def fetch_all(query, params=()):
    conn = get_db_connection()
    records = conn.execute(query, params).fetchall()
    conn.close()
    return records


def fetch_one(query, params=()):
    conn = get_db_connection()
    record = conn.execute(query, params).fetchone()
    conn.close()
    return record


def execute_query(query, params=()):
    conn = get_db_connection()
    conn.execute(query, params)
    conn.commit()
    conn.close()


def count_records(table_name):
    record = fetch_one(f"SELECT COUNT(*) AS total FROM {table_name}")
    return record["total"]


def get_recent_messages(limit=3):
    return fetch_all(
        """
        SELECT *
        FROM messages
        ORDER BY message_id DESC
        LIMIT ?
        """,
        (limit,)
    )


def get_unread_message_count(user_id):
    record = fetch_one(
        """
        SELECT last_seen_message_id
        FROM message_reads
        WHERE user_id = ?
        """,
        (user_id,)
    )

    last_seen = 0

    if record:
        last_seen = record["last_seen_message_id"]

    count = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM messages
        WHERE message_id > ?
        """,
        (last_seen,)
    )

    return count["total"]


def mark_messages_seen(user_id):
    latest = fetch_one("SELECT MAX(message_id) AS latest_id FROM messages")
    latest_id = latest["latest_id"] if latest and latest["latest_id"] else 0

    execute_query(
        """
        INSERT INTO message_reads (user_id, last_seen_message_id)
        VALUES (?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET last_seen_message_id = excluded.last_seen_message_id
        """,
        (user_id, latest_id)
    )


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["user_id"]
            session["name"] = user["name"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid login information.")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))

    recent_messages = get_recent_messages()
    unread_count = get_unread_message_count(session["user_id"])

    if session["role"] == "Student":
        return render_template(
            "student_dashboard.html",
            recent_messages=recent_messages,
            unread_count=unread_count
        )

    if session["role"] == "Instructor":
        return render_template(
            "instructor_dashboard.html",
            recent_messages=recent_messages,
            unread_count=unread_count
        )

    if session["role"] == "Administrator":
        return render_template("admin_dashboard.html")

    return redirect(url_for("login"))


@app.route("/message-board", methods=["GET", "POST"])
def message_board():
    if not role_required("Student", "Instructor"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        execute_query(
            """
            INSERT INTO messages
            (sender_id, sender_name, sender_role, recipient_role, group_name, message_type, message_text, sent_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                session["name"],
                session["role"],
                request.form["recipient_role"],
                request.form["group_name"],
                request.form["message_type"],
                request.form["message_text"],
                request.form["sent_date"]
            )
        )

        return redirect(url_for("message_board"))

    mark_messages_seen(session["user_id"])

    messages = fetch_all(
        """
        SELECT *
        FROM messages
        ORDER BY message_id DESC
        """
    )

    return render_template("message_board.html", messages=messages)


@app.route("/admin-chat-log")
def admin_chat_log():
    if not admin_required():
        return redirect(url_for("dashboard"))

    messages = fetch_all(
        """
        SELECT *
        FROM messages
        ORDER BY message_id DESC
        """
    )

    return render_template("admin_chat_log.html", messages=messages)


@app.route("/admin-reports")
def admin_reports():
    if not admin_required():
        return redirect(url_for("dashboard"))

    stats = {
        "Total Users": count_records("users"),
        "Total Courses": count_records("courses"),
        "Total Assignments": count_records("assignments"),
        "Total Submissions": count_records("submissions"),
        "Total Grades": count_records("grades"),
        "Total Feedback Records": count_records("feedback"),
        "Total Announcements": count_records("announcements"),
        "Total Lesson Plans": count_records("lesson_plans"),
        "Total Learning Objectives": count_records("learning_objectives"),
        "Total Messages": count_records("messages"),
    }

    return render_template("admin_reports.html", stats=stats)


@app.route("/courses")
def courses():
    if not login_required():
        return redirect(url_for("login"))

    courses = fetch_all("SELECT * FROM courses")
    return render_template("courses.html", courses=courses)


@app.route("/assignments")
def assignments():
    if not login_required():
        return redirect(url_for("login"))

    assignments = fetch_all("SELECT * FROM assignments")
    return render_template("assignments.html", assignments=assignments)


@app.route("/calendar")
def calendar():
    if not login_required():
        return redirect(url_for("login"))

    today = date.today()

    selected_month = request.args.get("month", today.month, type=int)
    selected_year = request.args.get("year", today.year, type=int)
    selected_view = request.args.get("view", "month")

    if selected_month < 1:
        selected_month = 12
        selected_year -= 1

    if selected_month > 12:
        selected_month = 1
        selected_year += 1

    previous_month = selected_month - 1
    previous_year = selected_year

    if previous_month < 1:
        previous_month = 12
        previous_year -= 1

    next_month = selected_month + 1
    next_year = selected_year

    if next_month > 12:
        next_month = 1
        next_year += 1

    month_name = py_calendar.month_name[selected_month]
    month_days = py_calendar.Calendar(firstweekday=6).monthdatescalendar(
        selected_year,
        selected_month
    )

    calendar_days = []

    for week in month_days:
        for day in week:
            calendar_days.append({
                "label": day.day,
                "date_value": day.isoformat(),
                "is_current_month": day.month == selected_month,
                "is_today": day == today
            })

    assignment_items = fetch_all("""
        SELECT
            assignments.assignment_id,
            assignments.title,
            assignments.due_date AS event_date,
            assignments.points_possible,
            courses.course_name
        FROM assignments
        JOIN courses ON assignments.course_id = courses.course_id
        ORDER BY assignments.due_date ASC
    """)

    manual_items = fetch_all("""
        SELECT
            calendar_events.event_id,
            calendar_events.title,
            calendar_events.description,
            calendar_events.event_date,
            calendar_events.event_type,
            users.name AS created_by_name
        FROM calendar_events
        LEFT JOIN users ON calendar_events.created_by = users.user_id
        ORDER BY calendar_events.event_date ASC
    """)

    calendar_events = {}

    for item in assignment_items:
        event_date = item["event_date"]

        if event_date not in calendar_events:
            calendar_events[event_date] = []

        calendar_events[event_date].append({
            "title": item["title"],
            "description": item["course_name"],
            "points_possible": item["points_possible"],
            "event_type": "Assignment Due",
            "source": "assignment",
            "event_id": None
        })

    for item in manual_items:
        event_date = item["event_date"]

        if event_date not in calendar_events:
            calendar_events[event_date] = []

        calendar_events[event_date].append({
            "title": item["title"],
            "description": item["description"],
            "points_possible": None,
            "event_type": item["event_type"],
            "source": "manual",
            "event_id": item["event_id"]
        })

    return render_template(
        "calendar.html",
        calendar_events=calendar_events,
        selected_view=selected_view,
        calendar_days=calendar_days,
        month_name=month_name,
        selected_month=selected_month,
        selected_year=selected_year,
        previous_month=previous_month,
        previous_year=previous_year,
        next_month=next_month,
        next_year=next_year,
        today_date=today.isoformat()
    )


@app.route("/add-calendar-event", methods=["GET", "POST"])
def add_calendar_event():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        execute_query(
            """
            INSERT INTO calendar_events
            (title, description, event_date, event_type, created_by)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                request.form["title"],
                request.form["description"],
                request.form["event_date"],
                request.form["event_type"],
                session["user_id"]
            )
        )

        return redirect(url_for("calendar"))

    return render_template("add_calendar_event.html")


@app.route("/delete-calendar-event/<int:event_id>")
def delete_calendar_event(event_id):
    if not role_required("Instructor", "Administrator"):
        return redirect(url_for("dashboard"))

    execute_query(
        "DELETE FROM calendar_events WHERE event_id = ?",
        (event_id,)
    )

    return redirect(url_for("calendar"))


@app.route("/announcements")
def announcements():
    if not login_required():
        return redirect(url_for("login"))

    announcements = fetch_all("SELECT * FROM announcements")
    return render_template("announcements.html", announcements=announcements)


@app.route("/grades")
def grades():
    if not login_required():
        return redirect(url_for("login"))

    grades = fetch_all("SELECT * FROM grades")
    return render_template("grades.html", grades=grades)


@app.route("/feedback")
def feedback():
    if not login_required():
        return redirect(url_for("login"))

    feedback = fetch_all("SELECT * FROM feedback")
    return render_template("feedback.html", feedback=feedback)


@app.route("/lesson-plans")
def lesson_plans():
    if not login_required():
        return redirect(url_for("login"))

    lesson_plans = fetch_all("SELECT * FROM lesson_plans")
    return render_template("lesson_plans.html", lesson_plans=lesson_plans)


@app.route("/learning-objectives")
def learning_objectives():
    if not login_required():
        return redirect(url_for("login"))

    objectives = fetch_all("SELECT * FROM learning_objectives")
    return render_template("learning_objectives.html", objectives=objectives)


@app.route("/submissions")
def submissions():
    if not admin_or_instructor_required():
        return redirect(url_for("dashboard"))

    submissions = fetch_all("""
        SELECT
            submissions.submission_id,
            assignments.title AS assignment_title,
            users.name AS student_name,
            submissions.submission_text,
            submissions.submission_date,
            submissions.status
        FROM submissions
        JOIN assignments ON submissions.assignment_id = assignments.assignment_id
        JOIN users ON submissions.student_id = users.user_id
    """)

    return render_template("submissions.html", submissions=submissions)


@app.route("/submit-assignment", methods=["GET", "POST"])
def submit_assignment():
    if not student_required():
        return redirect(url_for("dashboard"))

    assignments = fetch_all("SELECT * FROM assignments")

    if request.method == "POST":
        execute_query(
            """
            INSERT INTO submissions
            (assignment_id, student_id, submission_text, submission_date, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                request.form["assignment_id"],
                session["user_id"],
                request.form["submission_text"],
                request.form["submission_date"],
                "Submitted"
            )
        )

        return redirect(url_for("assignments"))

    return render_template("submit_assignment.html", assignments=assignments)


@app.route("/create-course", methods=["GET", "POST"])
def create_course():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        execute_query(
            "INSERT INTO courses (course_name, instructor, description) VALUES (?, ?, ?)",
            (
                request.form["course_name"],
                session["name"],
                request.form["description"]
            )
        )

        return redirect(url_for("courses"))

    return render_template("create_course.html")


@app.route("/create-assignment", methods=["GET", "POST"])
def create_assignment():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    courses = fetch_all("SELECT * FROM courses")

    if request.method == "POST":
        execute_query(
            """
            INSERT INTO assignments
            (course_id, title, due_date, points_possible)
            VALUES (?, ?, ?, ?)
            """,
            (
                request.form["course_id"],
                request.form["title"],
                request.form["due_date"],
                request.form["points_possible"]
            )
        )

        return redirect(url_for("assignments"))

    return render_template("create_assignment.html", courses=courses)


@app.route("/post-announcement", methods=["GET", "POST"])
def post_announcement():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    courses = fetch_all("SELECT * FROM courses")

    if request.method == "POST":
        execute_query(
            """
            INSERT INTO announcements
            (course_id, title, message, post_date)
            VALUES (?, ?, ?, ?)
            """,
            (
                request.form["course_id"],
                request.form["title"],
                request.form["message"],
                request.form["post_date"]
            )
        )

        return redirect(url_for("announcements"))

    return render_template("post_announcement.html", courses=courses)


@app.route("/enter-grade", methods=["GET", "POST"])
def enter_grade():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    assignments = fetch_all("SELECT * FROM assignments")
    students = fetch_all("SELECT * FROM users WHERE role = 'Student'")

    if request.method == "POST":
        execute_query(
            """
            INSERT INTO grades
            (assignment_id, student_id, score, comments)
            VALUES (?, ?, ?, ?)
            """,
            (
                request.form["assignment_id"],
                request.form["student_id"],
                request.form["score"],
                request.form["comments"]
            )
        )

        return redirect(url_for("grades"))

    return render_template("enter_grade.html", assignments=assignments, students=students)


@app.route("/provide-feedback", methods=["GET", "POST"])
def provide_feedback():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    assignments = fetch_all("SELECT * FROM assignments")
    students = fetch_all("SELECT * FROM users WHERE role = 'Student'")

    if request.method == "POST":
        execute_query(
            """
            INSERT INTO feedback
            (assignment_id, student_id, comments, post_date)
            VALUES (?, ?, ?, ?)
            """,
            (
                request.form["assignment_id"],
                request.form["student_id"],
                request.form["comments"],
                request.form["post_date"]
            )
        )

        return redirect(url_for("feedback"))

    return render_template("provide_feedback.html", assignments=assignments, students=students)


@app.route("/create-lesson-plan", methods=["GET", "POST"])
def create_lesson_plan():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    courses = fetch_all("SELECT * FROM courses")

    if request.method == "POST":
        execute_query(
            """
            INSERT INTO lesson_plans
            (course_id, title, content, upload_date)
            VALUES (?, ?, ?, ?)
            """,
            (
                request.form["course_id"],
                request.form["title"],
                request.form["content"],
                request.form["upload_date"]
            )
        )

        return redirect(url_for("lesson_plans"))

    return render_template("create_lesson_plan.html", courses=courses)


@app.route("/create-learning-objective", methods=["GET", "POST"])
def create_learning_objective():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    courses = fetch_all("SELECT * FROM courses")

    if request.method == "POST":
        execute_query(
            """
            INSERT INTO learning_objectives
            (course_id, description)
            VALUES (?, ?)
            """,
            (
                request.form["course_id"],
                request.form["description"]
            )
        )

        return redirect(url_for("learning_objectives"))

    return render_template("create_learning_objective.html", courses=courses)


@app.route("/manage-users")
def manage_users():
    if not admin_required():
        return redirect(url_for("dashboard"))

    users = fetch_all("SELECT * FROM users ORDER BY role, name")
    return render_template("manage_users.html", users=users)


@app.route("/create-user", methods=["GET", "POST"])
def create_user():
    if not admin_required():
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        execute_query(
            """
            INSERT INTO users
            (name, email, password, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                request.form["name"],
                request.form["email"],
                request.form["password"],
                request.form["role"]
            )
        )

        return redirect(url_for("manage_users"))

    return render_template("create_user.html")


@app.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if not admin_required():
        return redirect(url_for("dashboard"))

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    ).fetchone()

    if request.method == "POST":
        conn.execute(
            """
            UPDATE users
            SET name = ?, email = ?, password = ?, role = ?
            WHERE user_id = ?
            """,
            (
                request.form["name"],
                request.form["email"],
                request.form["password"],
                request.form["role"],
                user_id
            )
        )
        conn.commit()
        conn.close()

        return redirect(url_for("manage_users"))

    conn.close()
    return render_template("edit_user.html", user=user)


@app.route("/delete-user/<int:user_id>")
def delete_user(user_id):
    if not admin_required():
        return redirect(url_for("dashboard"))

    if user_id != session["user_id"]:
        execute_query("DELETE FROM users WHERE user_id = ?", (user_id,))

    return redirect(url_for("manage_users"))


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)