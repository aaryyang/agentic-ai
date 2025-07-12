#!/usr/bin/env python3
"""
Test script to verify API endpoints are working
"""
import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_status():
    """Test the status endpoint"""
    try:
        response = requests.get(f"{API_BASE}/agent/status")
        print(f"Status endpoint: {response.status_code}")
        if response.status_code == 200:
            print("✅ Status endpoint working")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Status endpoint failed: {response.text}")
    except Exception as e:
        print(f"❌ Status endpoint error: {e}")

def test_chat():
    """Test the chat endpoint"""
    try:
        payload = {
            "message": "Hello, can you help me?",
            "user_id": "test_user",
            "context": {}
        }
        response = requests.post(f"{API_BASE}/agent/chat", json=payload)
        print(f"Chat endpoint: {response.status_code}")
        if response.status_code == 200:
            print("✅ Chat endpoint working")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Chat endpoint failed: {response.text}")
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")

def test_delegation():
    """Test the delegation endpoint"""
    try:
        payload = {
            "agent_type": "sales",
            "task": "Qualify a new lead",
            "context": {"lead_name": "John Doe", "company": "Test Corp"}
        }
        response = requests.post(f"{API_BASE}/agent/delegate", json=payload)
        print(f"Delegation endpoint: {response.status_code}")
        if response.status_code == 200:
            print("✅ Delegation endpoint working")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Delegation endpoint failed: {response.text}")
    except Exception as e:
        print(f"❌ Delegation endpoint error: {e}")

if __name__ == "__main__":
    print("🚀 Testing API endpoints...")
    print("Make sure the server is running on http://localhost:8000")
    
    # Give server time to start
    time.sleep(2)
    
    print("\n1. Testing status endpoint...")
    test_status()
    
    print("\n2. Testing chat endpoint...")
    test_chat()
    
    print("\n3. Testing delegation endpoint...")
    test_delegation()
    
    print("\n✅ API testing complete!")
