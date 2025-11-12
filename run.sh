#!/bin/bash
# Quick run script for Hello Kitty Assistant

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run setup first: bash setup.sh"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ".env file not found!"
    echo "Please copy .env.example and configure it:"
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi

# Activate virtual environment and run
source venv/bin/activate
python hello_kitty_assistant.py
