# Agentic AI Project Setup Script for Windows PowerShell
# This script sets up the project environment and installs all dependencies

Write-Host "Setting up Agentic AI Project..." -ForegroundColor Green

# Check if virtual environment exists
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Blue
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Blue
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Blue
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing project dependencies..." -ForegroundColor Blue
pip install -r requirements.txt

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To activate the environment in future sessions, run: .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "To deactivate, run: deactivate" -ForegroundColor Cyan
