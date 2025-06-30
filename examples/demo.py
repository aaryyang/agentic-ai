"""
AI Agent System - Usage Examples and Demo
Run this script to see the AI Agent system in action
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

async def demo_basic_agent():
    """Demonstrate basic agent functionality"""
    print("🤖 Demo: Basic Agent Interaction")
    print("=" * 50)
    
    try:
        from core.engine.core_agent import CoreAIAgent
        
        # Mock environment for demo
        os.environ['OPENAI_API_KEY'] = 'demo-key'
        
        # Initialize agent (will use mock responses in demo mode)
        agent = CoreAIAgent()
        
        # Test basic interaction
        print("📝 Processing message: 'Help me qualify a new lead'")
        
        # In a real scenario, this would call OpenAI
        # For demo, we'll simulate the response
        response_data = {
            "agent_type": "core",
            "response": "I'll help you qualify the lead. Please provide the lead details including company name, contact information, budget, authority level, needs, and timeline (BANT criteria).",
            "actions_taken": ["analyze_request", "prepare_qualification_framework"],
            "metadata": {"demo_mode": True},
            "success": True
        }
        
        print(f"🎯 Agent Response: {response_data['response']}")
        print(f"⚡ Actions: {', '.join(response_data['actions_taken'])}")
        print()
        
    except Exception as e:
        print(f"❌ Error in basic agent demo: {e}")


async def demo_specialized_agents():
    """Demonstrate specialized agent capabilities"""
    print("🎯 Demo: Specialized Agents")
    print("=" * 50)
    
    agents = {
        "sales": "Lead qualification and pipeline management",
        "operations": "Process automation and optimization", 
        "quote": "Pricing calculations and quote generation",
        "scheduler": "Meeting scheduling and calendar management"
    }
    
    for agent_type, description in agents.items():
        print(f"🔧 {agent_type.title()} Agent: {description}")
    
    print("\n💡 Example delegation:")
    print("→ 'Delegate to sales agent: Qualify lead from Acme Corp'")
    print("→ 'Delegate to quote agent: Generate quote for 100 licenses'")
    print("→ 'Delegate to scheduler agent: Schedule demo for next week'")
    print()


async def demo_workflows():
    """Demonstrate workflow automation"""
    print("🔄 Demo: Workflow Automation")
    print("=" * 50)
    
    # Example workflow structure
    example_workflow = {
        "name": "Lead Qualification Workflow",
        "trigger_type": "webhook",
        "steps": [
            {
                "id": "receive_lead",
                "type": "agent_task",
                "parameters": {
                    "agent_type": "sales",
                    "task": "Extract and validate lead information"
                }
            },
            {
                "id": "qualify_lead", 
                "type": "agent_task",
                "parameters": {
                    "agent_type": "sales",
                    "task": "Apply BANT qualification criteria"
                }
            },
            {
                "id": "update_crm",
                "type": "crm_update",
                "parameters": {
                    "record_type": "lead",
                    "updates": {"status": "qualified", "score": "{{qualification_score}}"}
                }
            },
            {
                "id": "notify_sales",
                "type": "notification",
                "parameters": {
                    "message": "New qualified lead: {{lead_name}}",
                    "recipients": ["sales_team"]
                }
            }
        ]
    }
    
    print("📋 Example Workflow Structure:")
    print(json.dumps(example_workflow, indent=2))
    print()
    
    print("🚀 Workflow Execution Flow:")
    for i, step in enumerate(example_workflow["steps"], 1):
        print(f"  {i}. {step['id']}: {step['type']}")
    print()


async def demo_external_integrations():
    """Demonstrate external platform capabilities"""
    print("📱 Demo: External Platform Integrations")
    print("=" * 50)
    
    platforms = {
        "WhatsApp Business": {
            "features": ["Message handling", "Template messages", "Interactive buttons"],
            "webhook": "/whatsapp/webhook",
            "use_case": "Customer support via WhatsApp"
        },
        "Telegram Bot": {
            "features": ["Commands", "Callbacks", "Group chat support"],
            "webhook": "/telegram/webhook", 
            "use_case": "Team notifications and quick tasks"
        },
        "Web Chat": {
            "features": ["Session management", "Real-time messaging", "Embeddable widget"],
            "endpoint": "/webchat/message",
            "use_case": "Website customer assistance"
        }
    }
    
    for platform, details in platforms.items():
        print(f"🔌 {platform}:")
        print(f"   Features: {', '.join(details['features'])}")
        print(f"   Endpoint: {details.get('webhook', details.get('endpoint'))}")
        print(f"   Use Case: {details['use_case']}")
        print()


async def demo_api_endpoints():
    """Demonstrate API endpoints"""
    print("🌐 Demo: API Endpoints")
    print("=" * 50)
    
    endpoints = {
        "Core Agent": [
            "POST /agent/chat - Direct agent interaction",
            "POST /agent/delegate - Delegate to specialists", 
            "GET /agent/status - System status"
        ],
        "Workflow Management": [
            "POST /workflows/create - Create workflow",
            "POST /workflows/{id}/execute - Execute workflow",
            "GET /workflows - List all workflows"
        ],
        "Specialized Operations": [
            "POST /sales/qualify-lead - Lead qualification",
            "POST /quotes/generate - Quote generation",
            "POST /schedule/meeting - Meeting scheduling"
        ],
        "External Platforms": [
            "POST /whatsapp/webhook - WhatsApp messages",
            "POST /telegram/webhook - Telegram updates",
            "POST /webchat/message - Web chat messages"
        ]
    }
    
    for category, endpoint_list in endpoints.items():
        print(f"📁 {category}:")
        for endpoint in endpoint_list:
            print(f"   • {endpoint}")
        print()


async def demo_example_requests():
    """Show example API requests"""
    print("📝 Demo: Example API Requests")
    print("=" * 50)
    
    examples = {
        "Chat with Agent": {
            "method": "POST",
            "url": "/agent/chat",
            "payload": {
                "message": "Help me create a quote for 50 software licenses",
                "user_id": "user_123",
                "context": {"source": "web_portal"}
            }
        },
        "Delegate to Sales Agent": {
            "method": "POST", 
            "url": "/agent/delegate",
            "payload": {
                "agent_type": "sales",
                "task": "Qualify lead from Tech Startup Inc with $75k budget",
                "context": {"lead_source": "website_form"}
            }
        },
        "Create Workflow": {
            "method": "POST",
            "url": "/workflows/create", 
            "payload": {
                "workflow_name": "Quote Generation",
                "trigger_type": "manual",
                "steps": [
                    {
                        "type": "agent_task",
                        "parameters": {
                            "agent_type": "quote", 
                            "task": "Generate comprehensive quote"
                        }
                    }
                ]
            }
        }
    }
    
    for name, example in examples.items():
        print(f"🔥 {name}:")
        print(f"   {example['method']} {example['url']}")
        print(f"   Payload: {json.dumps(example['payload'], indent=6)}")
        print()


async def main():
    """Run all demos"""
    print("🚀 AI Agent System - Live Demo")
    print("=" * 60)
    print("This demo shows the capabilities of the LangChain-based")
    print("multi-agent AI system for CRM automation.")
    print("=" * 60)
    print()
    
    try:
        await demo_basic_agent()
        await demo_specialized_agents()
        await demo_workflows()
        await demo_external_integrations()
        await demo_api_endpoints()
        await demo_example_requests()
        
        print("🎉 Demo Complete!")
        print("=" * 50)
        print("🚀 To start the system:")
        print("   → Run: python -m uvicorn src.main:app --reload")
        print("   → Or: ./start.sh (Linux/Mac) or start.bat (Windows)")
        print("   → Or: docker-compose up")
        print()
        print("📖 API Documentation:")
        print("   → http://localhost:8000/docs")
        print()
        print("🔍 Health Check:")
        print("   → http://localhost:8000/health")
        print()
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Run the demo
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
