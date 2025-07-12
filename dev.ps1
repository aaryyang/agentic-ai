# Agentic AI Project - Development Environment
# This script activates the virtual environment and provides useful shortcuts

# Activate the virtual environment
& .\.venv\Scripts\Activate.ps1

# Set environment variables if .env file exists
if (Test-Path ".env") {
    Write-Host "Loading environment variables from .env file..." -ForegroundColor Green
    Get-Content .env | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]*)\s*=\s*(.*)\s*$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            Set-Item -Path "env:$name" -Value $value
        }
    }
}

Write-Host "Agentic AI Development Environment Ready!" -ForegroundColor Green
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  Start API Server: python -m uvicorn api.main:app --reload" -ForegroundColor White
Write-Host "  Interactive Chat: python scripts/interactive_chat.py" -ForegroundColor White
Write-Host "  Run Tests: pytest" -ForegroundColor White
Write-Host "  Code Formatting: black ." -ForegroundColor White
Write-Host "  Type Deactivate to exit the environment" -ForegroundColor White
