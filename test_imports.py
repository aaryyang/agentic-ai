#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

def test_core_agent():
    """Test CoreAIAgent import"""
    try:
        from core.engine.core_agent import CoreAIAgent
        print("✅ CoreAIAgent imported successfully")
        return True
    except ImportError as e:
        print(f"❌ CoreAIAgent import failed: {e}")
        return False

def test_api_routes():
    """Test API routes import"""
    try:
        from api.routes.agent import router
        print("✅ Agent router imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Agent router import failed: {e}")
        return False

def test_config():
    """Test config import"""
    try:
        from config.settings import Settings
        print("✅ Config imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False

def test_schemas():
    """Test schemas import"""
    try:
        from api.schemas.requests import ChatRequest
        from api.schemas.responses import AgentResponse
        print("✅ Schemas imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Schemas import failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Testing imports...")
    
    results = [
        test_config(),
        test_core_agent(),
        test_schemas(),
        test_api_routes()
    ]
    
    if all(results):
        print("\n🎉 All imports successful!")
    else:
        print("\n❌ Some imports failed!")
        
    # Try to test the full API
    try:
        from api.main import app
        print("✅ FastAPI app imported successfully")
        print("\n🚀 You can now start the server with:")
        print("   uvicorn api.main:app --reload --port 8000")
    except ImportError as e:
        print(f"❌ FastAPI app import failed: {e}")
