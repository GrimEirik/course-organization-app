@echo off
cd /d "%~dp0"

echo Starting Course Organization Application...
echo.

start http://127.0.0.1:5000

venv\bin\python.exe database.py
venv\bin\python.exe app.py

pause