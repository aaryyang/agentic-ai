"""
Example usage of the AI Agent system
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

# Load environment variables
load_dotenv()

from core.engine.core_agent import CoreAIAgent
from integrations.web_chat_integration import WebChatIntegration


async def example_basic_agent_interaction():
    """Example of basic agent interaction"""
    print("\\n=== Basic Agent Interaction ===")
    
    agent = CoreAIAgent()
    
    # Example conversations
    test_messages = [
        "Hello, I need help with generating a quote for CRM software",
        "Can you help me schedule a meeting with the sales team?",
        "What are your pricing plans for the AI agent system?",
        "I need to automate our lead qualification process"
    ]
    
    for message in test_messages:
        print(f"\\nUser: {message}")
        response = await agent.process_message(message, user_id="demo_user")
        print(f"Agent: {response.response}")
        if response.actions_taken:
            print(f"Actions: {', '.join(response.actions_taken)}")


async def example_specialist_delegation():
    """Example of delegating to specialist agents"""
    print("\\n=== Specialist Agent Delegation ===")
    
    agent = CoreAIAgent()
    
    # Sales agent example
    sales_response = await agent.delegate_to_specialist(
        agent_type="sales",
        task="Qualify this lead: Company ABC, budget $50k, timeline 3 months",
        context={"lead_source": "website", "priority": "high"}
    )
    print(f"\\nSales Agent: {sales_response.response}")
    
    # Operations agent example
    ops_response = await agent.delegate_to_specialist(
        agent_type="operations",
        task="Set up automation for lead follow-up emails",
        context={"frequency": "weekly", "template": "nurture_sequence"}
    )
    print(f"\\nOperations Agent: {ops_response.response}")
    
    # Quote agent example
    quote_response = await agent.delegate_to_specialist(
        agent_type="quote",
        task="Generate pricing for enterprise CRM solution",
        context={"users": 100, "integrations": 5, "support_level": "premium"}
    )
    print(f"\\nQuote Agent: {quote_response.response}")


async def example_web_chat_integration():
    """Example of web chat integration"""
    print("\\n=== Web Chat Integration ===")
    
    web_chat = WebChatIntegration()
    session_id = "demo_session_001"
    
    # Start session
    session = await web_chat.start_session(
        session_id, 
        user_info={"name": "John Doe", "email": "john@example.com"}
    )
    print(f"\\nSession started: {session['welcome_message']}")
    
    # Send messages
    messages = [
        "Hi, I'm interested in your CRM AI solution",
        "What's the pricing?",
        "Can you schedule a demo?"
    ]
    
    for message in messages:
        print(f"\\nUser: {message}")
        response = await web_chat.handle_message(session_id, message)
        print(f"Agent: {response['message']}")
        
        if 'suggested_actions' in response:
            print("Suggested actions:")
            for action in response['suggested_actions']:
                print(f"  - {action['text']}")
    
    # Handle action
    action_response = await web_chat.handle_action(
        session_id, 
        "get_quote",
        {"requirements": "Enterprise CRM with AI automation"}
    )
    print(f"\\nAction Result: {action_response['result']['message']}")


async def example_workflow_automation():
    """Example of workflow automation"""
    print("\\n=== Workflow Automation ===")
    
    agent = CoreAIAgent()
    
    # Define workflow steps
    workflow_steps = [
        {"step": 1, "action": "receive_lead", "trigger": "form_submission"},
        {"step": 2, "action": "qualify_lead", "criteria": ["budget", "authority", "need", "timeline"]},
        {"step": 3, "action": "assign_sales_rep", "logic": "round_robin"},
        {"step": 4, "action": "send_welcome_email", "template": "lead_welcome"},
        {"step": 5, "action": "schedule_follow_up", "delay": "24_hours"}
    ]
    
    # Set up automation
    response = await agent.delegate_to_specialist(
        agent_type="operations",
        task="Set up lead management workflow automation",
        context={"workflow_steps": workflow_steps, "priority": "high"}
    )
    
    print(f"\\nWorkflow Setup: {response.response}")


async def example_multi_platform_scenario():
    """Example of multi-platform customer interaction scenario"""
    print("\\n=== Multi-Platform Scenario ===")
    
    # Simulate a customer journey across platforms
    agent = CoreAIAgent()
    
    print("\\n1. Customer starts on website chat:")
    web_response = await agent.process_message(
        "I'm looking for a CRM solution for my small business",
        user_id="customer_123",
        context={"platform": "web_chat", "page": "pricing"}
    )
    print(f"Web Chat: {web_response.response}")
    
    print("\\n2. Customer continues conversation on WhatsApp:")
    whatsapp_response = await agent.process_message(
        "Hi, I was chatting on your website about CRM. Can you send me pricing details?",
        user_id="customer_123",
        context={"platform": "whatsapp", "phone": "+1234567890"}
    )
    print(f"WhatsApp: {whatsapp_response.response}")
    
    print("\\n3. Customer asks for demo via Telegram:")
    telegram_response = await agent.process_message(
        "Can you schedule a demo for me? I'm available this week",
        user_id="customer_123",
        context={"platform": "telegram", "chat_id": "789012345"}
    )
    print(f"Telegram: {telegram_response.response}")


async def main():
    """Run all examples"""
    print("AI Agent System - Example Usage")
    print("================================")
    
    try:
        await example_basic_agent_interaction()
        await example_specialist_delegation()
        await example_web_chat_integration()
        await example_workflow_automation()
        await example_multi_platform_scenario()
        
        print("\\n\\n=== Examples Complete ===")
        print("The AI Agent system is ready for production use!")
        
    except Exception as e:
        print(f"\\nError running examples: {str(e)}")
        print("Make sure you have set up your environment variables in .env file")


if __name__ == "__main__":
    asyncio.run(main())
