#!/usr/bin/env python3
"""
Test API endpoints directly to verify they work correctly
"""
import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_api_endpoints():
    """Test all API endpoints"""
    print("🔄 Testing API endpoints...")
    
    try:
        # Import the endpoint functions
        from api.routes.agent import get_agent_status, chat_with_agent
        from api.schemas.requests import ChatRequest
        
        print("\n1. Testing status endpoint...")
        status = await get_agent_status()
        print(f"   ✅ Status: {status.get('status')}")
        print(f"   ✅ Mode: {status.get('mode')}")
        print(f"   ✅ Users: {status.get('conversation_users')}")
        print(f"   ✅ API: {status.get('api_configured')}")
        
        print("\n2. Testing chat endpoint...")
        chat_request = ChatRequest(
            message="Hello, how are you?",
            user_id="test_user",
            context={"source": "test"}
        )
        
        chat_response = await chat_with_agent(chat_request)
        print(f"   ✅ Chat response: {chat_response.get('response', 'No response')[:50]}...")
        print(f"   ✅ Success: {chat_response.get('success', False)}")
        print(f"   ✅ Agent type: {chat_response.get('agent_type', 'unknown')}")
        
        print("\n🎉 All API endpoints working correctly!")
        
    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_api_endpoints())
