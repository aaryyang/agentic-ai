#!/bin/bash

# AI Agent System v2.0 Startup Script
# Organized Architecture Edition

echo "🚀 Starting AI Agent CRM System v2.0..."
echo "📁 Using new organized structure"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Set up environment variables
if [ ! -f ".env" ]; then
    echo "⚙️ Setting up environment variables..."
    cp .env.example .env
    echo "✏️ Please edit .env file with your API keys"
fi

# Start the application with new structure
echo "🌐 Starting FastAPI server..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "💚 Health Check: http://localhost:8000/health"
echo "ℹ️ System Info: http://localhost:8000/"

python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
