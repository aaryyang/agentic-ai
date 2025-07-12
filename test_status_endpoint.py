#!/usr/bin/env python3
"""
Test the status endpoint to verify it returns the correct data
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_status_endpoint():
    """Test the status endpoint logic"""
    print("🔄 Testing status endpoint...")
    
    try:
        # Import the status function
        from api.routes.agent import get_agent_status
        
        # Call the status endpoint
        status = await get_agent_status()
        
        print("✅ Status endpoint returned:")
        print(f"   Status: {status.get('status')}")
        print(f"   Mode: {status.get('mode')}")
        print(f"   API Configured: {status.get('api_configured')}")
        print(f"   Conversation Users: {status.get('conversation_users')}")
        print(f"   Core Agent: {status.get('core_agent')}")
        
        # Check if all required fields are present
        required_fields = ['status', 'mode', 'api_configured', 'conversation_users']
        missing_fields = [field for field in required_fields if field not in status]
        
        if missing_fields:
            print(f"❌ Missing fields: {missing_fields}")
        else:
            print("✅ All required fields present")
        
        return status
        
    except Exception as e:
        print(f"❌ Error testing status endpoint: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(test_status_endpoint())
