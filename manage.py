#!/usr/bin/env python3
"""
Management script for the Agentic AI system
Provides utilities for development and maintenance
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

def start_dev_server():
    """Start the development server"""
    print("🚀 Starting development server...")
    try:
        subprocess.run([
            "uvicorn", 
            "api.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

def check_environment():
    """Check the environment setup"""
    print("🔍 Checking environment...")
    try:
        subprocess.run([sys.executable, "check_env.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Environment check failed: {e}")
        sys.exit(1)

def install_deps():
    """Install dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def test_api():
    """Test API endpoints"""
    print("🧪 Testing API endpoints...")
    try:
        import requests
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ API health check passed")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            
    except ImportError:
        print("❌ requests library not available for testing")
    except Exception as e:
        print(f"❌ API test failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Agentic AI Management Script")
    parser.add_argument("command", choices=[
        "start", "check", "install", "test"
    ], help="Command to execute")
    
    args = parser.parse_args()
    
    if args.command == "start":
        start_dev_server()
    elif args.command == "check":
        check_environment()
    elif args.command == "install":
        install_deps()
    elif args.command == "test":
        test_api()

if __name__ == "__main__":
    main()