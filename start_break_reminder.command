#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment and run the application
cd "$SCRIPT_DIR" && source venv/bin/activate && python break_reminder.py 