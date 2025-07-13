"""
Environment check script for debugging Render deployment
"""

import os
import sys
from pathlib import Path

print("🔍 Environment Check - Agentic AI")
print("=" * 50)

# Python Info
print(f"Python Version: {sys.version}")
print(f"Python Path: {sys.executable}")

# Environment Variables
print("\n📝 Environment Variables:")
env_vars = [
    "GROQ_API_KEY", "GROQ_MODEL", "SECRET_KEY", 
    "DEBUG", "REQUIRE_API_KEY", "API_KEY", "CORS_ORIGINS"
]

for var in env_vars:
    value = os.getenv(var)
    if var == "GROQ_API_KEY" and value:
        # Hide most of the API key for security
        masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
        print(f"  {var}: {masked}")
    else:
        print(f"  {var}: {value}")

# Check project structure
print("\n📁 Project Structure:")
project_root = Path(__file__).parent
print(f"  Project Root: {project_root}")

key_files = [
    "api/main.py",
    "core/engine/core_agent_simple.py", 
    "config/settings.py",
    "requirements.txt"
]

for file_path in key_files:
    full_path = project_root / file_path
    exists = "✅" if full_path.exists() else "❌"
    print(f"  {exists} {file_path}")

# Try importing key modules
print("\n📦 Module Imports:")
modules = [
    ("fastapi", "FastAPI"),
    ("groq", "Groq"),
    ("pydantic", "BaseModel"),
    ("pydantic_settings", "BaseSettings"),
    ("structlog", "get_logger"),
    ("uvicorn", "run")
]

for module_name, class_name in modules:
    try:
        module = __import__(module_name)
        if hasattr(module, class_name):
            print(f"  ✅ {module_name}.{class_name}")
        else:
            print(f"  ⚠️  {module_name} (missing {class_name})")
    except ImportError as e:
        print(f"  ❌ {module_name}: {e}")

# Try initializing Groq client
print("\n🤖 Groq Client Test:")
try:
    from groq import Groq
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        try:
            client = Groq(api_key=api_key)
            print("  ✅ Groq client initialized successfully")
        except Exception as e:
            print(f"  ❌ Groq client error: {e}")
    else:
        print("  ⚠️  GROQ_API_KEY not set")
except ImportError as e:
    print(f"  ❌ Groq import error: {e}")

print("\n✅ Environment check completed!")
