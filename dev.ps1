# AI Agent CRM - PowerShell Development Script
# Usage: .\dev.ps1

param(
    [string]$Command = "dev"
)

function Show-Help {
    Write-Host "🤖 AI Agent CRM - Available Commands:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  .\dev.ps1 dev      - Start development server (default)" -ForegroundColor Green
    Write-Host "  .\dev.ps1 start    - Start production server" -ForegroundColor Green
    Write-Host "  .\dev.ps1 prod     - Start production server with workers" -ForegroundColor Green
    Write-Host "  .\dev.ps1 chat     - Start interactive chat terminal" -ForegroundColor Green
    Write-Host "  .\dev.ps1 test     - Run tests" -ForegroundColor Green
    Write-Host "  .\dev.ps1 install  - Install dependencies" -ForegroundColor Green
    Write-Host "  .\dev.ps1 clean    - Clean cache files" -ForegroundColor Green
    Write-Host "  .\dev.ps1 lint     - Lint and format code" -ForegroundColor Green
    Write-Host "  .\dev.ps1 help     - Show this help" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 URLs:" -ForegroundColor Yellow
    Write-Host "  Dashboard: http://localhost:8000/dashboard" -ForegroundColor White
    Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor White
}

function Start-DevServer {
    Write-Host "🚀 Starting AI Agent CRM Development Server..." -ForegroundColor Green
    Write-Host "📡 Server will be available at: http://localhost:8000" -ForegroundColor Yellow
    Write-Host "🖥️  Web Dashboard: http://localhost:8000/dashboard" -ForegroundColor Yellow
    Write-Host "📚 API Documentation: http://localhost:8000/docs" -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Cyan
    Write-Host "---"
    
    uvicorn api.main:app --reload --port 8000 --host 0.0.0.0
}

function Start-ProdServer {
    Write-Host "🚀 Starting AI Agent CRM Production Server..." -ForegroundColor Green
    uvicorn api.main:app --port 8000 --host 0.0.0.0
}

function Start-ProdServerWithWorkers {
    Write-Host "🚀 Starting AI Agent CRM Production Server with Workers..." -ForegroundColor Green
    uvicorn api.main:app --port 8000 --host 0.0.0.0 --workers 4
}

function Start-Chat {
    Write-Host "💬 Starting Interactive Chat..." -ForegroundColor Green
    python scripts/interactive_chat.py
}

function Run-Tests {
    Write-Host "🧪 Running Tests..." -ForegroundColor Green
    pytest tests/ -v
}

function Install-Dependencies {
    Write-Host "📦 Installing Dependencies..." -ForegroundColor Green
    pip install -r requirements.txt
}

function Clean-Cache {
    Write-Host "🧹 Cleaning Cache Files..." -ForegroundColor Green
    Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force
    Get-ChildItem -Path . -Recurse -File -Name "*.pyc" | Remove-Item -Force
    Write-Host "✅ Cache cleaned!" -ForegroundColor Green
}

function Lint-Code {
    Write-Host "🔍 Linting and Formatting Code..." -ForegroundColor Green
    black .
    flake8 .
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "dev" { Start-DevServer }
    "start" { Start-ProdServer }
    "prod" { Start-ProdServerWithWorkers }
    "chat" { Start-Chat }
    "test" { Run-Tests }
    "install" { Install-Dependencies }
    "clean" { Clean-Cache }
    "lint" { Lint-Code }
    "help" { Show-Help }
    default { 
        Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
        Show-Help 
    }
}
