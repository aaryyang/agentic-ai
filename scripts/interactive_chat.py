#!/usr/bin/env python3
"""
Interactive AI Agent Testing Interface
Run this to chat with your AI agent directly
"""
import sys
import os
import asyncio

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine.core_agent import CoreAIAgent

class InteractiveAgent:
    def __init__(self):
        self.agent = CoreAIAgent()
        self.user_id = "interactive_user"
        
    async def start_chat(self):
        """Start interactive chat session"""
        print("🤖 AI Agent System - Interactive Chat")
        print("=" * 50)
        
        if self.agent.groq_client is None:
            print("⚠️  Running in MOCK mode - configure GROQ_API_KEY for real responses")
        else:
            print(f"✅ Connected to Groq - Model: {self.agent.model}")
        
        print("\nCommands:")
        print("  'quit' or 'exit' - Exit the chat")
        print("  'status' - Show system status")
        print("  'delegate [type] [task]' - Delegate to specialist")
        print("  'clear' - Clear conversation memory")
        print("\nStart chatting! Type your message and press Enter.")
        print("-" * 50)
        
        while True:
            try:
                # Get user input
                user_input = input("\n🧑 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                
                elif user_input.lower() == 'status':
                    status = self.agent.get_status()
                    print(f"\n📊 System Status:")
                    for key, value in status.items():
                        print(f"   {key}: {value}")
                    continue
                
                elif user_input.lower() == 'clear':
                    self.agent.clear_memory(self.user_id)
                    print("🧹 Conversation memory cleared!")
                    continue
                
                elif user_input.lower().startswith('delegate'):
                    await self.handle_delegation(user_input)
                    continue
                
                # Process normal message
                print("🤖 Agent: ", end="", flush=True)
                response = await self.agent.process_message(
                    message=user_input,
                    user_id=self.user_id,
                    context={"interface": "interactive"}
                )
                
                print(response.response)
                
                if response.actions_taken:
                    print(f"📋 Actions: {', '.join(response.actions_taken)}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
    
    async def handle_delegation(self, command):
        """Handle delegation commands"""
        parts = command.split(' ', 2)
        if len(parts) < 3:
            print("Usage: delegate [sales/operations/quote/scheduler] [task description]")
            return
        
        agent_type = parts[1]
        task = parts[2]
        
        print(f"🔄 Delegating to {agent_type} agent...")
        response = await self.agent.delegate_to_specialist(
            agent_type=agent_type,
            task=task,
            context={"interface": "interactive"}
        )
        
        print(f"🤖 {agent_type.title()} Agent: {response.response}")

async def main():
    """Main function"""
    try:
        chat = InteractiveAgent()
        await chat.start_chat()
    except Exception as e:
        print(f"❌ Failed to start interactive chat: {str(e)}")
        print("Make sure you're in the correct directory and have installed dependencies.")

if __name__ == "__main__":
    asyncio.run(main())
