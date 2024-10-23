# Define the app directory
$APP_DIR = ".\app"

# Check if the app directory exists
if (-Not (Test-Path $APP_DIR)) {
    Write-Host "[ERROR] - '$APP_DIR' directory not found."
    exit 1
}

# Define the virtual environment path
$VENV_PATH = "$APP_DIR\.venv"

# Check if virtual environment exists
if (-Not (Test-Path $VENV_PATH)) {
    Write-Host "[STATUS] - Creating virtual environment in '$VENV_PATH'..."
    python -m venv $VENV_PATH
    
    # Check if the venv was successfully created
    if (-Not (Test-Path $VENV_PATH)) {
        Write-Host "[ERROR] - Failed to create the virtual environment."
        exit 1
    }

    Write-Host "[STATUS] - Virtual environment created."
}

# Check if the activate script exists
$ACTIVATE_SCRIPT = "$VENV_PATH\Scripts\Activate.ps1"
if (-Not (Test-Path $ACTIVATE_SCRIPT)) {
    Write-Host "[ERROR] - Activation script not found in '$ACTIVATE_SCRIPT'."
    exit 1
}

# Activate the virtual environment
Write-Host "[STATUS] - Activating the virtual environment..."
& $ACTIVATE_SCRIPT

# Upgrade pip inside the virtual environment
Write-Host "[STATUS] - Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
$REQUIREMENTS_FILE = "$APP_DIR\requirements.txt"

if (Test-Path $REQUIREMENTS_FILE) {
    Write-Host "[STATUS] - Installing requirements from '$REQUIREMENTS_FILE'..."
    python -m pip install -r $REQUIREMENTS_FILE
} else {
    Write-Host "[ERROR] - '$REQUIREMENTS_FILE' not found."
    exit 1
}

# Run the FastAPI application
Write-Host "[STATUS] - Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
