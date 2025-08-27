#!/bin/bash

echo "Quiz Master - Flask Application"
echo "==============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed or not in PATH"
    exit 1
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "Starting the Quiz Master application..."
echo "======================================="
echo "🚀 The application will be available at: http://localhost:5000"
echo "📧 Default admin login: admin@quizmaster.com"
echo "🔑 Default admin password: admin123"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
