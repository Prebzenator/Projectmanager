@echo off
REM Project Planner Web Application Launcher
REM This script starts the Flask backend for the web application

setlocal enabledelayedexpansion

REM Find Python executable
set PYTHON_PATH=C:\Users\truls\AppData\Local\Python\bin\python3.exe

REM Check if Flask is installed
echo Checking dependencies...
!PYTHON_PATH! -m pip show flask >nul 2>&1

if errorlevel 1 (
    echo Flask not installed. Installing dependencies...
    !PYTHON_PATH! -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Error installing dependencies
        pause
        exit /b 1
    )
)

echo.
echo ============================================
echo  PROJECT PLANNER - WEB APPLICATION
echo ============================================
echo.
echo Starting Flask server...
echo.
echo Open your browser and go to:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

!PYTHON_PATH! app.py

pause
