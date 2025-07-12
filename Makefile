# AI Agent CRM - Makefile
# Usage: make dev, make start, make install, etc.

.PHONY: dev start prod chat test install clean lint help

# Default target
.DEFAULT_GOAL := help

# Development server with auto-reload
dev:
	@echo "🚀 Starting development server..."
	uvicorn api.main:app --reload --port 8000 --host 0.0.0.0

# Production server
start:
	@echo "🚀 Starting production server..."
	uvicorn api.main:app --port 8000 --host 0.0.0.0

# Production server with multiple workers
prod:
	@echo "🚀 Starting production server with workers..."
	uvicorn api.main:app --port 8000 --host 0.0.0.0 --workers 4

# Interactive chat terminal
chat:
	@echo "💬 Starting interactive chat..."
	python scripts/interactive_chat.py

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	@echo "📦 Installing development dependencies..."
	pip install -r requirements.txt
	pip install -e .[dev]

# Clean cache files
clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Lint and format code
lint:
	@echo "🔍 Linting and formatting code..."
	black .
	flake8 .

# Show help
help:
	@echo "AI Agent CRM - Available Commands:"
	@echo ""
	@echo "  make dev       - Start development server (with auto-reload)"
	@echo "  make start     - Start production server"
	@echo "  make prod      - Start production server with workers"
	@echo "  make chat      - Start interactive chat terminal"
	@echo "  make test      - Run tests"
	@echo "  make install   - Install dependencies"
	@echo "  make clean     - Clean cache files"
	@echo "  make lint      - Lint and format code"
	@echo "  make help      - Show this help message"
	@echo ""
	@echo "🌐 URLs:"
	@echo "  Dashboard: http://localhost:8000/dashboard"
	@echo "  API Docs:  http://localhost:8000/docs"
