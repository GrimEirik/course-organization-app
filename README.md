# Course Organization Application

## COM-430 Software Engineering Project

### Team Members

* Steven Runion
* [Add Additional Team Members Here]

---

# Project Overview

The Course Organization Application is a web-based Learning Management System (LMS) prototype developed using:

* Python 3
* Flask
* SQLite
* HTML/CSS
* GitHub
* Jenkins
* Pytest

The application provides role-based access for:

### Student

* View Courses
* View Assignments
* Submit Assignments
* View Announcements
* View Grades
* View Feedback
* View Lesson Plans
* View Learning Objectives

### Instructor

* Create Courses
* Create Assignments
* Post Announcements
* Enter Grades
* Provide Feedback
* Create Lesson Plans
* Create Learning Objectives
* View Student Submissions

### Administrator

* View Courses
* View Assignments
* View Submissions
* View Grades
* View Feedback
* View Lesson Plans
* View Learning Objectives

---

# Repository

Clone the repository:

```bash
git clone https://github.com/GrimEirik/course-organization-app.git
```

Enter the project directory:

```bash
cd course-organization-app
```

---

# Windows Installation Guide

## Step 1: Install Python

Download and install Python 3.12 or newer:

https://www.python.org/downloads/

During installation:

✓ Check "Add Python to PATH"

Verify installation:

```bash
python --version
```

Expected output:

```text
Python 3.12.x
```

---

## Step 2: Create Virtual Environment

Inside the project folder:

```bash
python -m venv venv
```

---

## Step 3: Activate Virtual Environment

Command Prompt:

```bash
venv\Scripts\activate
```

Git Bash:

```bash
source venv/Scripts/activate
```

Expected:

```text
(venv)
```

appears at the beginning of the terminal prompt.

---

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 5: Build Database

```bash
python database.py
```

Expected:

```text
Database initialized successfully.
```

---

## Step 6: Run Application

```bash
python app.py
```

Expected:

```text
Running on http://127.0.0.1:5000
```

Open:

http://127.0.0.1:5000

---

# macOS Installation Guide

## Step 1: Verify Python

Open Terminal:

```bash
python3 --version
```

If Python is missing:

https://www.python.org/downloads/macos/

---

## Step 2: Create Virtual Environment

Inside the project directory:

```bash
python3 -m venv venv
```

---

## Step 3: Activate Virtual Environment

```bash
source venv/bin/activate
```

Expected:

```text
(venv)
```

appears at the beginning of the terminal prompt.

---

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

If needed:

```bash
pip3 install -r requirements.txt
```

---

## Step 5: Build Database

```bash
python3 database.py
```

Expected:

```text
Database initialized successfully.
```

---

## Step 6: Run Application

```bash
python3 app.py
```

Open:

http://127.0.0.1:5000

---

# Test Accounts

## Student

Email:

```text
student@test.com
```

Password:

```text
password
```

---

## Instructor

Email:

```text
instructor@test.com
```

Password:

```text
password
```

---

## Administrator

Email:

```text
admin@test.com
```

Password:

```text
password
```

---

# Running Automated Tests

Run:

```bash
pytest
```

Expected:

```text
12 passed
```

(or higher depending on future development)

---

# Jenkins Pipeline

The Jenkins pipeline performs:

1. Checkout Source Code
2. Install Dependencies
3. Initialize Database
4. Run Automated Tests
5. Validate Build

Expected Jenkins result:

```text
Finished: SUCCESS
```

---

# Git Workflow

Create a feature branch:

```bash
git checkout -b feature-name
```

Example:

```bash
git checkout -b feature-student-submissions
```

Commit changes:

```bash
git add .
git commit -m "Describe your changes"
```

Push branch:

```bash
git push origin feature-name
```

Create a Pull Request in GitHub for review.

Do not commit directly to the main branch.

---

# Common Troubleshooting

## Flask Not Found

Activate virtual environment:

Windows:

```bash
venv\Scripts\activate
```

macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Database Error

Delete:

```text
database/course_app.db
```

Then rebuild:

```bash
python database.py
```

---

## Port Already In Use

Stop the running Flask process or restart the terminal.

---

# Project Architecture

```text
User
  ↓
Flask Web Application
  ↓
SQLite Database
  ↓
GitHub Repository
  ↓
Jenkins CI/CD Pipeline
```

---

# Current Features

✓ Authentication

✓ Student Dashboard

✓ Instructor Dashboard

✓ Administrator Dashboard

✓ Course Management

✓ Assignment Management

✓ Assignment Submission System

✓ Grade Tracking

✓ Feedback System

✓ Lesson Plans

✓ Learning Objectives

✓ Announcements

✓ SQLite Database

✓ Automated Testing

✓ Jenkins Continuous Integration

✓ GitHub Source Control
