#!/usr/bin/env python3
"""
Test the status endpoint logic directly
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Test the status endpoint logic
try:
    from api.routes.agent import get_agent_status
    import asyncio
    
    async def test_status():
        print("🔄 Testing status endpoint...")
        try:
            status = await get_agent_status()
            print("✅ Status endpoint working!")
            print(f"Status: {status}")
            return True
        except Exception as e:
            print(f"❌ Status endpoint error: {e}")
            return False
    
    # Run the test
    result = asyncio.run(test_status())
    if result:
        print("\n🎉 Status endpoint test passed!")
    else:
        print("\n❌ Status endpoint test failed!")
        
except Exception as e:
    print(f"❌ Failed to import status endpoint: {e}")
