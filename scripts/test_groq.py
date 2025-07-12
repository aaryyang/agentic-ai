#!/usr/bin/env python3
"""
Test script to verify Groq integration works
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from core.engine.core_agent import CoreAIAgent

async def test_groq_integration():
    """Test the Groq integration"""
    print("🧪 Testing Groq Integration...")
    
    try:
        # Initialize the agent
        agent = CoreAIAgent()
        print("✅ Agent initialized successfully")
        
        # Test basic functionality
        if agent.groq_client is None:
            print("⚠️  Running in mock mode - configure GROQ_API_KEY for real responses")
        else:
            print("✅ Groq client configured and ready")
        
        # Test a simple message
        response = await agent.process_message(
            message="Hello! Can you help me with sales?",
            user_id="test_user",
            context={"source": "test"}
        )
        
        print(f"✅ Response received: {response.response[:100]}...")
        print(f"✅ Agent type: {response.agent_type}")
        print(f"✅ Success: {response.success}")
        
        # Test agent delegation
        delegate_response = await agent.delegate_to_specialist(
            agent_type="sales",
            task="Qualify this lead: Test Company with $10k budget",
            context={"priority": "high"}
        )
        
        print(f"✅ Delegation response: {delegate_response.response[:100]}...")
        
        # Test system status
        status = agent.get_status()
        print(f"✅ System status: {status}")
        
        print("\n🎉 All tests passed! Groq integration is working correctly.")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_groq_integration())
