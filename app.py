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


def instructor_required():
    return "user_id" in session and session["role"] == "Instructor"


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

    role = session["role"]

    if role == "Student":
        return render_template("student_dashboard.html")

    if role == "Instructor":
        return render_template("instructor_dashboard.html")

    if role == "Administrator":
        return render_template("admin_dashboard.html")

    return redirect(url_for("login"))


@app.route("/courses")
def courses():
    if not login_required():
        return redirect(url_for("login"))

    conn = get_db_connection()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()

    return render_template("courses.html", courses=courses)


@app.route("/assignments")
def assignments():
    if not login_required():
        return redirect(url_for("login"))

    conn = get_db_connection()
    assignments = conn.execute("SELECT * FROM assignments").fetchall()
    conn.close()

    return render_template("assignments.html", assignments=assignments)


@app.route("/announcements")
def announcements():
    if not login_required():
        return redirect(url_for("login"))

    conn = get_db_connection()
    announcements = conn.execute("SELECT * FROM announcements").fetchall()
    conn.close()

    return render_template("announcements.html", announcements=announcements)


@app.route("/grades")
def grades():
    if not login_required():
        return redirect(url_for("login"))

    conn = get_db_connection()
    grades = conn.execute("SELECT * FROM grades").fetchall()
    conn.close()

    return render_template("grades.html", grades=grades)


@app.route("/feedback")
def feedback():
    if not login_required():
        return redirect(url_for("login"))

    conn = get_db_connection()
    feedback = conn.execute("SELECT * FROM feedback").fetchall()
    conn.close()

    return render_template("feedback.html", feedback=feedback)


@app.route("/create-course", methods=["GET", "POST"])
def create_course():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        course_name = request.form["course_name"]
        description = request.form["description"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO courses (course_name, instructor, description) VALUES (?, ?, ?)",
            (course_name, session["name"], description)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("courses"))

    return render_template("create_course.html")


@app.route("/create-assignment", methods=["GET", "POST"])
def create_assignment():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    conn = get_db_connection()
    courses = conn.execute("SELECT * FROM courses").fetchall()

    if request.method == "POST":
        course_id = request.form["course_id"]
        title = request.form["title"]
        due_date = request.form["due_date"]
        points_possible = request.form["points_possible"]

        conn.execute(
            "INSERT INTO assignments (course_id, title, due_date, points_possible) VALUES (?, ?, ?, ?)",
            (course_id, title, due_date, points_possible)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("assignments"))

    conn.close()
    return render_template("create_assignment.html", courses=courses)


@app.route("/post-announcement", methods=["GET", "POST"])
def post_announcement():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    conn = get_db_connection()
    courses = conn.execute("SELECT * FROM courses").fetchall()

    if request.method == "POST":
        course_id = request.form["course_id"]
        title = request.form["title"]
        message = request.form["message"]
        post_date = request.form["post_date"]

        conn.execute(
            "INSERT INTO announcements (course_id, title, message, post_date) VALUES (?, ?, ?, ?)",
            (course_id, title, message, post_date)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("announcements"))

    conn.close()
    return render_template("post_announcement.html", courses=courses)


@app.route("/enter-grade", methods=["GET", "POST"])
def enter_grade():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    conn = get_db_connection()
    assignments = conn.execute("SELECT * FROM assignments").fetchall()
    students = conn.execute("SELECT * FROM users WHERE role = 'Student'").fetchall()

    if request.method == "POST":
        assignment_id = request.form["assignment_id"]
        student_id = request.form["student_id"]
        score = request.form["score"]
        comments = request.form["comments"]

        conn.execute(
            "INSERT INTO grades (assignment_id, student_id, score, comments) VALUES (?, ?, ?, ?)",
            (assignment_id, student_id, score, comments)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("grades"))

    conn.close()
    return render_template("enter_grade.html", assignments=assignments, students=students)


@app.route("/provide-feedback", methods=["GET", "POST"])
def provide_feedback():
    if not instructor_required():
        return redirect(url_for("dashboard"))

    conn = get_db_connection()
    assignments = conn.execute("SELECT * FROM assignments").fetchall()
    students = conn.execute("SELECT * FROM users WHERE role = 'Student'").fetchall()

    if request.method == "POST":
        assignment_id = request.form["assignment_id"]
        student_id = request.form["student_id"]
        comments = request.form["comments"]
        post_date = request.form["post_date"]

        conn.execute(
            "INSERT INTO feedback (assignment_id, student_id, comments, post_date) VALUES (?, ?, ?, ?)",
            (assignment_id, student_id, comments, post_date)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("feedback"))

    conn.close()
    return render_template("provide_feedback.html", assignments=assignments, students=students)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)