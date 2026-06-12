import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


def test_login_page_loads():
    tester = app.test_client()
    response = tester.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_home_redirects_to_login():
    tester = app.test_client()
    response = tester.get("/")
    assert response.status_code == 302


def test_dashboard_requires_login():
    tester = app.test_client()
    response = tester.get("/dashboard")
    assert response.status_code == 302


def test_courses_requires_login():
    tester = app.test_client()
    response = tester.get("/courses")
    assert response.status_code == 302


def test_assignments_requires_login():
    tester = app.test_client()
    response = tester.get("/assignments")
    assert response.status_code == 302


def test_announcements_requires_login():
    tester = app.test_client()
    response = tester.get("/announcements")
    assert response.status_code == 302


def test_grades_requires_login():
    tester = app.test_client()
    response = tester.get("/grades")
    assert response.status_code == 302


def test_feedback_requires_login():
    tester = app.test_client()
    response = tester.get("/feedback")
    assert response.status_code == 302


def test_lesson_plans_requires_login():
    tester = app.test_client()
    response = tester.get("/lesson-plans")
    assert response.status_code == 302


def test_learning_objectives_requires_login():
    tester = app.test_client()
    response = tester.get("/learning-objectives")
    assert response.status_code == 302


def test_submit_assignment_requires_student_login():
    tester = app.test_client()
    response = tester.get("/submit-assignment")
    assert response.status_code == 302


def test_submissions_requires_instructor_or_admin_login():
    tester = app.test_client()
    response = tester.get("/submissions")
    assert response.status_code == 302


def test_admin_reports_requires_admin_login():
    tester = app.test_client()
    response = tester.get("/admin-reports")
    assert response.status_code == 302


def test_manage_users_requires_admin_login():
    tester = app.test_client()
    response = tester.get("/manage-users")
    assert response.status_code == 302

    def test_calendar_requires_login():
    tester = app.test_client()
    response = tester.get("/calendar")
    assert response.status_code == 302