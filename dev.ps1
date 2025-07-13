# Development startup script for Windows PowerShell
# Quick way to start the development server

Write-Host "Starting Agentic AI Development Server..." -ForegroundColor Green

# Check if virtual environment exists
if (Test-Path ".venv") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "No virtual environment found. Creating one..." -ForegroundColor Yellow
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt
}

# Start the development server
Write-Host "Starting FastAPI development server..." -ForegroundColor Green
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000