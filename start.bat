@echo off
chcp 936 >nul
:: ============================================================
:: Auto Macro Tool Launcher
:: ============================================================

title Auto Macro Tool Launcher
color 0A

set "APP_NAME=Auto Macro Tool"
set "PYTHON_SCRIPT=main.py"
set "VENV_DIR=venv"

cd /d "%~dp0"

echo.
echo ========================================
echo    %APP_NAME% Launcher
echo ========================================
echo.

:: Step 1: Check main file
echo [1/3] Checking main file...
if not exist "%PYTHON_SCRIPT%" (
    color 0C
    echo [ERROR] Main file not found: %PYTHON_SCRIPT%
    echo Current directory: %CD%
    pause
    exit /b 1
)
echo [OK] Main file found.

:: Step 2: Check Python
echo.
echo [2/3] Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        color 0C
        echo [ERROR] Python not found.
        echo Please install Python 3.8 or higher.
        echo Download: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        set "PYTHON_CMD=python3"
    )
) else (
    set "PYTHON_CMD=python"
)
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo [OK] Python %PYTHON_VERSION% detected.

:: Step 3: Check virtual environment
echo.
echo [3/3] Checking virtual environment...
if exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment...
    call "%VENV_DIR%\Scripts\activate.bat" >nul 2>&1
    echo [OK] Virtual environment activated.
) else (
    echo [INFO] No virtual environment found, using system Python.
)

:: Launch application
echo.
echo ========================================
echo    Launching %APP_NAME%...
echo ========================================
echo.

color 07
%PYTHON_CMD% "%PYTHON_SCRIPT%"

set "EXIT_CODE=%errorlevel%"

echo.
if %EXIT_CODE% equ 0 (
    color 0A
    echo [OK] Application exited normally.
) else (
    color 0C
    echo [ERROR] Application exited with code: %EXIT_CODE%
)

echo.
echo Press any key to close...
pause >nul

exit /b %EXIT_CODE%
