#!/bin/bash
# Script to set up the project
# Mostly written by Courtney Jackson with the help of Claude Sonnet 4 for error handling improvements

set -e  # Exit on any error

echo "======================================"
echo "ConfSpotter Setup Script"
echo "======================================"
echo ""

# Check for conda
if ! command -v conda &> /dev/null; then
    echo "Error: conda not found. Please install Anaconda or Miniconda."
    exit 1
fi

eval "$(conda shell.bash hook)"
conda activate base

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setting up the database..."
mysql -u ConfSpotter -pchickenlittle < SQL/shell.sql 2>&1 | grep -v "Warning" | grep -v "already exists" || true
wait
mysql -u ConfSpotter -pchickenlittle confspotter < "SQL/SecurityFeatures.sql" 2>&1 | grep -v "Warning" | grep -v "already exists" | grep -v "SUPER privilege" || true
wait
mysql -u ConfSpotter -pchickenlittle confspotter < "SQL/sample_project_data.sql" 2>&1 | grep -v "Warning" | grep -v "Duplicate entry" || true
wait
mysql -u ConfSpotter -pchickenlittle confspotter < "SQL/Stored_Procedures and Triggers.sql" 2>&1 | grep -v "Warning" || true
wait

echo "Populating database..."
$CONDA_PREFIX/bin/python "Python/Scraping V3.py" || true
wait
$CONDA_PREFIX/bin/python "Python/clean_conference_data.py" || true
wait
$CONDA_PREFIX/bin/python "Python/PaperScrapping.py" || true
wait
$CONDA_PREFIX/bin/python "Python/csv-conversion-script.py" || true
wait

echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

$CONDA_PREFIX/bin/python app.py


