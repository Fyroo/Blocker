#!/bin/bash

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi



# Install dependencies
echo "Installing dependencies..."
# Activate virtual environment
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
echo "Setup completed successfully!"
exit
