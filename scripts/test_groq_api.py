#!/usr/bin/env python3
"""
Test Groq API directly
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_groq_api():
    """Test Groq API directly"""
    try:
        from groq import Groq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or "placeholder" in api_key:
            print("❌ GROQ_API_KEY not configured properly")
            print("Please set a valid Groq API key in your .env file")
            return False
        
        print("🧪 Testing Groq API directly...")
        
        client = Groq(api_key=api_key)
        
        # Test a simple completion
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "user", "content": "Say hello and confirm you are working!"}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        response = completion.choices[0].message.content
        print(f"✅ Groq API Response: {response}")
        print("🎉 Groq integration is working perfectly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Groq API: {str(e)}")
        return False

if __name__ == "__main__":
    test_groq_api()
