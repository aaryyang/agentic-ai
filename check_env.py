#!/usr/bin/env python3
"""
Environment checker for Agentic AI system
Validates all required environment variables and dependencies
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if the environment is properly configured"""
    print("🔍 Checking Agentic AI Environment...")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version OK")
    
    # Check required files
    required_files = [
        "requirements.txt",
        "api/main.py",
        "core/engine/core_agent_simple.py",
        ".env.example"
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} found")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    # Check environment variables
    env_vars = [
        "GROQ_API_KEY",
    ]
    
    print("\n🔑 Environment Variables:")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * (len(value) - 4) + value[-4:]}")
        else:
            print(f"⚠️  {var}: Not set (optional for development)")
    
    # Check if virtual environment is active
    print(f"\n🐍 Virtual Environment: {'✅ Active' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else '⚠️ Not active'}")
    
    print("\n" + "=" * 50)
    print("🎉 Environment check complete!")
    return True

if __name__ == "__main__":
    try:
        check_environment()
    except Exception as e:
        print(f"❌ Error checking environment: {e}")
        sys.exit(1)