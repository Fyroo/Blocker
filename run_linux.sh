#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Setup not completed. Running setup script..."
    chmod +x setup_linux.sh
    ./setup_linux.sh
fi

# Activate virtual environment
source venv/bin/activate

# Start the Python program
sudo python src/__main__.py
deactivate
exit
