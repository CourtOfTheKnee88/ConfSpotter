@echo off
REM Script to set up the project on Windows
REM Orginal script written by Courtney Jackson converted to Windows batch by Claude Sonnet 4

echo ======================================
echo ConfSpotter Setup Script
echo ======================================
echo.

REM Check for conda
where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: conda not found. Please install Anaconda or Miniconda.
    exit /b 1
)

echo Installing dependencies...
call conda activate base
pip install -r requirements.txt

echo.
echo Setting up the database...
mysql -u ConfSpotter -pchickenlittle < SQL\shell.sql 2>&1 | findstr /V "Warning already exists" || ver >nul
mysql -u ConfSpotter -pchickenlittle confspotter < "SQL\SecurityFeatures.sql" 2>&1 | findstr /V "Warning already exists SUPER privilege" || ver >nul
mysql -u ConfSpotter -pchickenlittle confspotter < "SQL\sample_project_data.sql" 2>&1 | findstr /V "Warning Duplicate entry" || ver >nul
mysql -u ConfSpotter -pchickenlittle confspotter < "SQL\Stored_Procedures and Triggers.sql" 2>&1 | findstr /V "Warning" || ver >nul

echo.
echo Populating database...
python "Python\Scraping V3.py" >nul 2>&1 || ver >nul
python "Python\clean_conference_data.py" >nul 2>&1 || ver >nul
python "Python\PaperScrapping.py" >nul 2>&1 || ver >nul
python "Python\csv-conversion-script.py" >nul 2>&1 || ver >nul

echo.
echo Installing frontend dependencies...
cd frontend
call npm install
cd ..