#!/bin/bash

# Define the app directory
APP_DIR="./app"

# Check if the app directory exists
if [ ! -d "$APP_DIR" ]; then
    echo "[ERROR] - '$APP_DIR' directory not found."
    exit 1
fi

# Define the virtual environment path
VENV_PATH="$APP_DIR/.venv"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "[STATUS] - Creating virtual environment in '$VENV_PATH'..."
    python3 -m venv "$VENV_PATH"
    
    # Check if the venv was successfully created
    if [ ! -d "$VENV_PATH" ]; then
        echo "[ERROR] - Failed to create the virtual environment."
        exit 1
    fi

    echo "[STATUS] - Virtual environment created."
fi

# Check if the activate script exists
ACTIVATE_SCRIPT="$VENV_PATH/bin/activate"
if [ ! -f "$ACTIVATE_SCRIPT" ]; then
    echo "[ERROR] - Activation script not found in '$ACTIVATE_SCRIPT'."
    exit 1
fi

# Activate the virtual environment
echo "[STATUS] - Activating the virtual environment..."
source "$ACTIVATE_SCRIPT"

# Check if activation succeeded
if [ $? -ne 0 ]; then
    echo "[STATUS] - [ERROR] - Failed to activate the virtual environment."
    exit 1
fi

# Upgrade pip inside the virtual environment
echo "[STATUS] - Upgrading pip..."
python3 -m pip install --upgrade pip

# Install requirements
REQUIREMENTS_FILE="$APP_DIR/requirements.txt"

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "[STATUS] - Installing requirements from '$REQUIREMENTS_FILE'..."
    python -m pip install -r "$REQUIREMENTS_FILE"
else
    echo "[ERROR] - '$REQUIREMENTS_FILE' not found."
    exit 1
fi

# Run the FastAPI application
echo "[STATUS] - Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
