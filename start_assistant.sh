#!/bin/bash
# Start Hello Kitty Assistant with clean output

cd "/home/shehriyar-ali-rustam/Personal Assitant (Hello Kitty)"
source venv/bin/activate

# Suppress ALSA warnings for cleaner output
export PYTHONUNBUFFERED=1

echo "Starting Hello Kitty Assistant..."
echo "Press Ctrl+C to stop"
echo ""

# Run with filtered output (remove ALSA warnings)
python -u hello_kitty_assistant.py 2>&1 | grep -v "ALSA\|jack\|JackShm\|Cannot connect"
