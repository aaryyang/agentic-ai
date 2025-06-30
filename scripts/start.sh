#!/bin/bash

# AI Agent System Startup Script

echo "🤖 Starting AI Agent System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before running the system."
    echo "📝 Required: OPENAI_API_KEY"
    echo "📝 Optional: TELEGRAM_BOT_TOKEN, WHATSAPP_API_TOKEN"
fi

# Check if Redis is running
if ! pgrep -x "redis-server" > /dev/null; then
    echo "⚠️  Redis is not running. Starting Redis..."
    if command -v redis-server &> /dev/null; then
        redis-server --daemonize yes
        echo "✅ Redis started successfully"
    else
        echo "❌ Redis is not installed. Please install Redis or use Docker Compose."
        echo "💡 Alternative: Run 'docker-compose up' to start with Docker"
        exit 1
    fi
fi

# Start the application
echo "🚀 Starting AI Agent System..."
echo "📍 API will be available at: http://localhost:8000"
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the system"

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
