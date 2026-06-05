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

        return render_template(
            "login.html",
            error="Invalid login information."
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if not login_required():
        return redirect(url_for("login"))

    role = session["role"]

    if role == "Student":
        return render_template("student_dashboard.html")

    elif role == "Instructor":
        return render_template("instructor_dashboard.html")

    elif role == "Administrator":
        return render_template("admin_dashboard.html")

    return redirect(url_for("login"))


@app.route("/courses")
def courses():

    if not login_required():
        return redirect(url_for("login"))

    conn = get_db_connection()

    courses = conn.execute(
        "SELECT * FROM courses"
    ).fetchall()

    conn.close()

    return render_template(
        "courses.html",
        courses=courses
    )


@app.route("/assignments")
def assignments():

    if not login_required():
        return redirect(url_for("login"))

    conn = get_db_connection()

    assignments = conn.execute(
        "SELECT * FROM assignments"
    ).fetchall()

    conn.close()

    return render_template(
        "assignments.html",
        assignments=assignments
    )


@app.route("/announcements")
def announcements():

    if not login_required():
        return redirect(url_for("login"))

    conn = get_db_connection()

    announcements = conn.execute(
        "SELECT * FROM announcements"
    ).fetchall()

    conn.close()

    return render_template(
        "announcements.html",
        announcements=announcements
    )


@app.route("/grades")
def grades():

    if not login_required():
        return redirect(url_for("login"))

    conn = get_db_connection()

    grades = conn.execute(
        "SELECT * FROM grades"
    ).fetchall()

    conn.close()

    return render_template(
        "grades.html",
        grades=grades
    )


@app.route("/feedback")
def feedback():

    if not login_required():
        return redirect(url_for("login"))

    conn = get_db_connection()

    feedback = conn.execute(
        "SELECT * FROM feedback"
    ).fetchall()

    conn.close()

    return render_template(
        "feedback.html",
        feedback=feedback
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)