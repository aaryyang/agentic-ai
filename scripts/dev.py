#!/usr/bin/env python3
"""
Development server startup script
Usage: python scripts/dev.py
"""
import subprocess
import sys
import os

def main():
    """Start the development server with reload enabled"""
    print("🚀 Starting AI Agent CRM Development Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🖥️  Web Dashboard: http://localhost:8000/dashboard")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("---")
    
    # Change to project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    try:
        # Start uvicorn with reload for development
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "api.main:app",
            "--reload",
            "--port", "8000",
            "--host", "0.0.0.0"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Development server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
