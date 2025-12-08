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

# Load environment variables from .env file
if [ -f .env ]; then
    echo "Loading database configuration from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found. Please create one based on the template."
    exit 1
fi

# Set default values if not provided in .env
DB_HOST=${DB_HOST:-localhost}
DB_USER=${DB_USER:-ConfSpotter}
DB_PASSWORD=${DB_PASSWORD:-chickenlittle}
DB_NAME=${DB_NAME:-confspotter}
DB_PORT=${DB_PORT:-3306}

echo "Setting up the database..."
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" < SQL/shell.sql 2>&1 | grep -v "Warning" | grep -v "already exists" || true
wait
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "SQL/SecurityFeatures.sql" 2>&1 | grep -v "Warning" | grep -v "already exists" | grep -v "SUPER privilege" || true
wait
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "SQL/sample_project_data.sql" 2>&1 | grep -v "Warning" | grep -v "Duplicate entry" || true
wait
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "SQL/Stored_Procedures and Triggers.sql" 2>&1 | grep -v "Warning" || true
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


