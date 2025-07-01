#!/bin/bash

echo "Class Manager Application - Unix/Linux/macOS Launcher"
echo "====================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r local_requirements.txt

# Set default environment variables if not set
export PGHOST=${PGHOST:-localhost}
export PGDATABASE=${PGDATABASE:-class_manager}
export PGUSER=${PGUSER:-postgres}
export PGPORT=${PGPORT:-5432}

# Display environment info
echo ""
echo "Environment Variables:"
echo "PGHOST=$PGHOST"
echo "PGDATABASE=$PGDATABASE"
echo "PGUSER=$PGUSER"
echo "PGPORT=$PGPORT"
echo ""

# Check if PGPASSWORD is set
if [ -z "$PGPASSWORD" ]; then
    echo "WARNING: PGPASSWORD is not set!"
    echo "Please set it as an environment variable or in a .env file"
    echo ""
fi

echo "Starting Streamlit application..."
echo "Open your browser to: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""
streamlit run main.py