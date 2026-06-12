from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

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


def execute_query(query, params=()):
    conn = get_db_connection()
    conn.execute(query, params)
    conn.commit()
    conn.close()


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

    if session["role"] == "Student":
        return render_template("student_dashboard.html")

    if session["role"] == "Instructor":
        return render_template("instructor_dashboard.html")

    if session["role"] == "Administrator":
        return render_template("admin_dashboard.html")

    return redirect(url_for("login"))


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


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)