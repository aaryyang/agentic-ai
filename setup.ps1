# Environment setup script for development
# Sets up Python virtual environment and installs dependencies

Write-Host "Setting up Agentic AI Development Environment..." -ForegroundColor Green

# Create virtual environment
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists. Removing old one..." -ForegroundColor Yellow
    Remove-Item .venv -Recurse -Force
}

Write-Host "Creating new virtual environment..." -ForegroundColor Yellow
python -m venv .venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "Setup complete! Run 'dev.ps1' to start the development server." -ForegroundColor Green