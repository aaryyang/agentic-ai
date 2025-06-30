@echo off
REM AI Agent System v2.0 Startup Script
REM Organized Architecture Edition

echo 🚀 Starting AI Agent CRM System v2.0...
echo 📁 Using new organized structure

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Set up environment variables
if not exist ".env" (
    echo ⚙️ Setting up environment variables...
    copy .env.example .env
    echo ✏️ Please edit .env file with your API keys
)

REM Start the application with new structure
echo 🌐 Starting FastAPI server...
echo 📖 API Documentation: http://localhost:8000/docs
echo 💚 Health Check: http://localhost:8000/health
echo ℹ️ System Info: http://localhost:8000/

python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

pause
