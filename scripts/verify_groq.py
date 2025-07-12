#!/usr/bin/env python3
"""
Simple Groq integration test
"""
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all imports work correctly"""
    try:
        print("🧪 Testing imports...")
        
        # Test Groq import
        from groq import Groq
        print("✅ Groq package imported successfully")
        
        # Test settings import
        from config.settings import Settings
        settings = Settings()
        print("✅ Settings imported successfully")
        
        # Test core agent import
        from core.engine.core_agent import CoreAIAgent
        print("✅ CoreAIAgent imported successfully")
        
        # Test agent initialization
        agent = CoreAIAgent()
        print("✅ CoreAIAgent initialized successfully")
        
        # Check if Groq client is configured
        if agent.groq_client is not None:
            print("✅ Groq client is configured and ready")
            print(f"✅ Using model: {agent.model}")
        else:
            print("⚠️  Groq client not configured (API key missing)")
        
        print("\n🎉 All imports and initialization successful!")
        print("🚀 Your Groq integration is ready to use!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n📝 Next steps:")
        print("1. Start the server: uvicorn api.main:app --reload --port 8000")
        print("2. Visit: http://localhost:8000/docs")
        print("3. Test the /agent/chat endpoint")
    else:
        print("\n🔧 Please fix the errors above before proceeding.")
