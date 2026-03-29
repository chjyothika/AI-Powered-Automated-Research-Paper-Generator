@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo AI-Powered Research Paper Generator - Setup ^& Run
echo ===================================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH.
    echo Please install Python 3.8 or newer and try again.
    pause
    exit /b 1
)

:: Define the virtual environment directory name
set "VENV_DIR=venv"

:: Check if the virtual environment exists
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Virtual environment not found. Creating '%VENV_DIR%'...
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [INFO] Virtual environment created successfully.
) else (
    echo [INFO] Virtual environment found.
)

:: Activate the virtual environment
echo [INFO] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

:: Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

:: Install dependencies
echo [INFO] Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies. Please check your requirements.txt.
    pause
    exit /b 1
)
echo [INFO] Dependencies are up to date.

:: Run the application
echo ===================================================
echo Starting the Streamlit application...
echo ===================================================
streamlit run app.py

:: Pause if the app exits or crashes
pause
