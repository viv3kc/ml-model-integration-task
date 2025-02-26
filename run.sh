#!/bin/bash

# Function to find next available port
find_available_port() {
    local port=8000
    while lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; do
        port=$((port + 1))
    done
    echo $port
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Find available port
PORT=$(find_available_port)
echo "Using port: $PORT"

# Run the application
echo "Starting the application..."
python main.py --port $PORT

# Note: The script will keep running until you stop the application
