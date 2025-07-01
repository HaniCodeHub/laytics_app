@echo off
echo Class Manager Application - Windows Launcher
echo =============================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r local_requirements.txt

REM Set default environment variables if not set
if not defined PGHOST set PGHOST=localhost
if not defined PGDATABASE set PGDATABASE=class_manager
if not defined PGUSER set PGUSER=postgres
if not defined PGPORT set PGPORT=5432

REM Display environment info
echo.
echo Environment Variables:
echo PGHOST=%PGHOST%
echo PGDATABASE=%PGDATABASE%
echo PGUSER=%PGUSER%
echo PGPORT=%PGPORT%
echo.

REM Check if PGPASSWORD is set
if not defined PGPASSWORD (
    echo WARNING: PGPASSWORD is not set!
    echo Please set it as an environment variable or in a .env file
    echo.
)

echo Starting Streamlit application...
echo Open your browser to: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
streamlit run main.py

pause