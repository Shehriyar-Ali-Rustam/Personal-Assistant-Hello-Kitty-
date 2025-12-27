#!/bin/bash

# Hello Kitty Web Chat - Run Script

echo "=========================================="
echo "  🎀 Hello Kitty Web Chat 🎀"
echo "=========================================="

# Navigate to web_app directory
cd "$(dirname "$0")"

# Check if virtual environment exists in parent directory
if [ -d "../venv" ]; then
    echo "📦 Activating virtual environment..."
    source ../venv/bin/activate
fi

# Install requirements if needed
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt

# Run the application
echo ""
echo "🚀 Starting server..."
echo "📡 Open http://localhost:5000 in your browser"
echo ""
python app.py
