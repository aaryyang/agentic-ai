@echo off
REM AI Agent System Startup Script for Windows

echo 🤖 Starting AI Agent System...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚙️  Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your API keys before running the system.
    echo 📝 Required: OPENAI_API_KEY
    echo 📝 Optional: TELEGRAM_BOT_TOKEN, WHATSAPP_API_TOKEN
)

REM Check if Redis is available
redis-cli ping >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Redis is not running.
    echo 💡 Please start Redis manually or use Docker Compose:
    echo    Option 1: Install and start Redis locally
    echo    Option 2: Run 'docker-compose up' to start with Docker
    echo.
    echo ❓ Do you want to continue without Redis? (y/n)
    set /p choice=
    if /i not "%choice%"=="y" exit /b 1
)

REM Start the application
echo 🚀 Starting AI Agent System...
echo 📍 API will be available at: http://localhost:8000
echo 📖 API Documentation: http://localhost:8000/docs
echo 🔍 Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the system

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
