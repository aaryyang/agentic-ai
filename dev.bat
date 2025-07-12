@echo off
REM AI Agent CRM - Development Server Batch Script

echo 🚀 Starting AI Agent CRM Development Server...
echo 📡 Server will be available at: http://localhost:8000
echo 🖥️  Web Dashboard: http://localhost:8000/dashboard  
echo 📚 API Documentation: http://localhost:8000/docs
echo Press Ctrl+C to stop the server
echo ---

uvicorn api.main:app --reload --port 8000 --host 0.0.0.0

pause
