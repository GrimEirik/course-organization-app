# Course Organization & Management Application

## COM-430 Software Engineering Project

This project is a web-based Course Organization & Management Application built for COM-430 Software Engineering. The application supports students, instructors, and administrators through separate role-based dashboards.

The system includes course management, assignments, assignment submissions, grading, feedback, announcements, lesson plans, learning objectives, a calendar system, message board, message notifications, administrative reports, and user management.

---

# Technology Stack

This application uses:

* Python
* Flask
* SQLite
* HTML
* CSS
* Git
* GitHub
* Pytest
* Jenkins

---

# Main Features

## Student Features

Students can:

* Log in to the student dashboard
* View courses
* View assignments
* Submit assignments
* View grades
* View instructor feedback
* View announcements
* View lesson plans
* View learning objectives
* View assignment calendar
* Use the message board
* See unread message notifications

## Instructor Features

Instructors can:

* Log in to the instructor dashboard
* Create courses
* Create assignments
* Post announcements
* Create lesson plans
* Create learning objectives
* Review student submissions
* Enter grades
* Provide feedback
* Add calendar events
* Use the message board
* View unread message notifications

## Administrator Features

Administrators can:

* Log in to the administrator dashboard
* Manage users
* View system reports
* Audit courses
* Audit assignments
* Audit submissions
* Audit grades
* Audit feedback
* Audit lesson plans
* Audit learning objectives
* Audit announcements
* View chat/message logs

---

# Demo Login Accounts

Use these accounts after the application is running.

## Student Account

Email:

```text
student@test.com
```

Password:

```text
password
```

## Instructor Account

Email:

```text
instructor@test.com
```

Password:

```text
password
```

## Administrator Account

Email:

```text
admin@test.com
```

Password:

```text
password
```

---

# Repository Setup

## Step 1: Clone the Repository

Open a terminal or command prompt and run:

```bash
git clone https://github.com/GrimEirik/course-organization-app.git
```

Move into the project folder:

```bash
cd course-organization-app
```

---

# Windows Setup Instructions

These steps are for Windows users using Command Prompt, PowerShell, or Git Bash.

## Step 1: Install Python

Download Python from:

```text
https://www.python.org/downloads/
```

During installation, make sure to check:

```text
Add Python to PATH
```

Verify Python installed correctly:

```bash
python --version
```

Expected result:

```text
Python 3.12.x
```

or newer.

---

## Step 2: Create a Virtual Environment

From inside the project folder, run:

```bash
python -m venv venv
```

This creates a local Python environment named:

```text
venv
```

---

## Step 3: Activate the Virtual Environment

### Command Prompt

```bash
venv\Scripts\activate
```

### PowerShell

```bash
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try again:

```bash
venv\Scripts\Activate.ps1
```

### Git Bash

Most Windows virtual environments use:

```bash
source venv/Scripts/activate
```

Some Git Bash environments may use:

```bash
source venv/bin/activate
```

If one does not work, try the other.

After activation, the terminal should show:

```text
(venv)
```

or:

```text
((venv))
```

---

## Step 4: Install Required Packages

Run:

```bash
pip install -r requirements.txt
```

This installs Flask, pytest, and other required packages.

---

## Step 5: Initialize the Database

Run:

```bash
python database.py
```

Expected output:

```text
Database initialized successfully.
```

This creates the SQLite database file inside the `database` folder.

---

## Step 6: Run the Application

Run:

```bash
python app.py
```

Expected output:

```text
Running on http://127.0.0.1:5000
```

Open a browser and go to:

```text
http://127.0.0.1:5000
```

---

# macOS Setup Instructions

These steps are for macOS users using Terminal.

## Step 1: Install Python

Check if Python 3 is installed:

```bash
python3 --version
```

If Python is not installed, download it from:

```text
https://www.python.org/downloads/macos/
```

---

## Step 2: Clone the Repository

```bash
git clone https://github.com/GrimEirik/course-organization-app.git
```

Move into the project folder:

```bash
cd course-organization-app
```

---

## Step 3: Create a Virtual Environment

```bash
python3 -m venv venv
```

---

## Step 4: Activate the Virtual Environment

```bash
source venv/bin/activate
```

The terminal should now show:

```text
(venv)
```

---

## Step 5: Install Required Packages

```bash
pip install -r requirements.txt
```

If needed, use:

```bash
pip3 install -r requirements.txt
```

---

## Step 6: Initialize the Database

```bash
python3 database.py
```

Expected output:

```text
Database initialized successfully.
```

---

## Step 7: Run the Application

```bash
python3 app.py
```

Open a browser and go to:

```text
http://127.0.0.1:5000
```

---

# Running Automated Tests

The project uses pytest for automated testing.

Make sure the virtual environment is activated first.

Run:

```bash
pytest
```

Expected result:

```text
tests passed
```

The exact number of tests may increase as the project grows.

---

# Common Issues and Fixes

## Problem: No module named Flask

This means the virtual environment is not activated or dependencies were not installed.

Fix:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python app.py
```

If using Git Bash, make sure the correct virtual environment is active:

```bash
source venv/bin/activate
```

or:

```bash
source venv/Scripts/activate
```

---

## Problem: Database Table Does Not Exist

This usually means the database was not initialized after code changes.

Fix:

```bash
python database.py
```

If the error continues, delete the old database file:

```text
database/course_app.db
```

Then run:

```bash
python database.py
```

---

## Problem: Port Already in Use

If Flask says port 5000 is already in use, another copy of the application may still be running.

Stop the running Flask server with:

```text
CTRL + C
```

Then restart:

```bash
python app.py
```

---

## Problem: Git Bash Uses the Wrong Python

If Git Bash uses the wrong Python, run:

```bash
which python
```

If it points to MSYS or another Python installation, activate the virtual environment:

```bash
source venv/bin/activate
```

or run the app directly with:

```bash
venv/bin/python app.py
```

---

# Project Folder Structure

The project is organized as follows:

```text
course-organization-app/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── Jenkinsfile
│
├── database/
│   └── course_app.db
│
├── static/
│   └── style.css
│
├── templates/
│   ├── login.html
│   ├── student_dashboard.html
│   ├── instructor_dashboard.html
│   ├── admin_dashboard.html
│   ├── courses.html
│   ├── assignments.html
│   ├── submissions.html
│   ├── grades.html
│   ├── feedback.html
│   ├── announcements.html
│   ├── lesson_plans.html
│   ├── learning_objectives.html
│   ├── calendar.html
│   ├── message_board.html
│   ├── admin_chat_log.html
│   ├── admin_reports.html
│   ├── contact.html
│   ├── privacy.html
│   └── about.html
│
└── tests/
    └── test_app.py
```

---

# Development Workflow

For team members contributing to the project:

## Step 1: Pull the Latest Code

```bash
git pull
```

## Step 2: Create a Feature Branch

```bash
git checkout -b feature-name
```

Example:

```bash
git checkout -b calendar-improvements
```

## Step 3: Make Changes

Edit the needed files.

## Step 4: Run Tests

```bash
pytest
```

## Step 5: Commit Changes

```bash
git add .
git commit -m "Describe the change made"
```

## Step 6: Push the Branch

```bash
git push origin feature-name
```

## Step 7: Create a Pull Request

Open GitHub and create a pull request into the main branch.

---

# Jenkins Pipeline

This project includes a Jenkins pipeline using the `Jenkinsfile`.

The pipeline performs:

1. Pull latest code from GitHub
2. Install dependencies
3. Initialize the database
4. Run automated tests
5. Report build success or failure

A successful Jenkins build should show:

```text
Finished: SUCCESS
```

---

# Application Workflow Summary

## Student Workflow

```text
Login
↓
Student Dashboard
↓
View Courses / Assignments / Calendar
↓
Submit Assignment
↓
View Grades and Feedback
↓
Use Message Board
```

## Instructor Workflow

```text
Login
↓
Instructor Dashboard
↓
Create Course Content
↓
Create Assignments
↓
Add Calendar Events
↓
Review Submissions
↓
Enter Grades and Feedback
↓
Communicate Through Message Board
```

## Administrator Workflow

```text
Login
↓
Administrator Dashboard
↓
Manage Users
↓
View System Reports
↓
Audit Records
↓
Review Chat Log
```

---

# Notes

This application is a student project prototype. It is intended for educational use and should not be used with real student records or sensitive personal data.

For production use, future improvements should include:

* Password hashing
* Stronger input validation
* Better session security
* Database migration tools
* Cloud deployment
* User enrollment management
* File uploads
* Full audit logging
