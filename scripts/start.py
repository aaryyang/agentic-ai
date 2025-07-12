#!/usr/bin/env python3
"""
Production server startup script
Usage: python scripts/start.py
"""
import subprocess
import sys
import os

def main():
    """Start the production server"""
    print("🚀 Starting AI Agent CRM Production Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("---")
    
    # Change to project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    try:
        # Start uvicorn for production (no reload, multiple workers)
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "api.main:app",
            "--port", "8000",
            "--host", "0.0.0.0",
            "--workers", "4"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Production server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
