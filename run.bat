@echo off
REM Project Planner - Interactive Mode Launcher
REM This script launches the Project Planner application

setlocal enabledelayedexpansion

REM Find Python executable
set PYTHON_PATH=C:\Users\truls\AppData\Local\Python\bin\python3.exe

REM Check if Python exists
if not exist "!PYTHON_PATH!" (
    echo Error: Python not found at !PYTHON_PATH!
    echo Please install Python or update the path.
    pause
    exit /b 1
)

REM Run the application
!PYTHON_PATH! projectplanner.py

pause
