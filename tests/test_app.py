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