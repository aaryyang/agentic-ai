# CRM Integration Guide

## Overview
This AI Agent system provides REST API endpoints that can be integrated into any CRM system. The agent specializes in sales, operations, quotes, and scheduling automation.

## Authentication Methods

### Option 1: No Authentication (Development/Testing)
- Set `REQUIRE_API_KEY=false` in environment variables
- Direct access to all endpoints without credentials
- **Use only for development or internal networks**

### Option 2: API Key Authentication (Recommended for Production)
- Set `REQUIRE_API_KEY=true` in environment variables
- Set `API_KEY=your_secure_api_key` in environment variables
- Include API key in Authorization header: `Authorization: Bearer your_api_key`

## Available Endpoints

### Base URL
```
https://your-agent-service.onrender.com
```

### Core Agent Endpoints

#### 1. Chat with Agent
```http
POST /agent/chat
Authorization: Bearer your_api_key
Content-Type: application/json

{
  "message": "I need to qualify this lead: John Doe from TechCorp",
  "user_id": "crm_user_123",
  "context": {
    "lead_id": "lead_456",
    "company": "TechCorp",
    "contact_name": "John Doe"
  }
}
```

**Response:**
```json
{
  "response": "I'll help you qualify this lead. Based on the company TechCorp...",
  "agent_type": "sales",
  "success": true,
  "metadata": {
    "qualification_score": 8.5,
    "next_actions": ["schedule_demo", "send_proposal"]
  }
}
```

#### 2. Delegate to Specialist Agent
```http
POST /agent/delegate
Authorization: Bearer your_api_key
Content-Type: application/json

{
  "agent_type": "sales",
  "task": "qualify_lead",
  "data": {
    "lead_id": "lead_456",
    "company": "TechCorp",
    "contact_info": {...}
  },
  "user_id": "crm_user_123"
}
```

### Workflow Automation

#### Create Workflow
```http
POST /workflows/create
Authorization: Bearer your_api_key
Content-Type: application/json

{
  "workflow_name": "lead_qualification_flow",
  "trigger_type": "new_lead",
  "steps": [
    {"action": "analyze_lead", "agent": "sales"},
    {"action": "score_lead", "criteria": "company_size,budget,timeline"},
    {"action": "assign_next_action", "conditions": {...}}
  ],
  "parameters": {
    "auto_assign": true,
    "notify_sales": true
  }
}
```

## Integration Examples

### CRM Webhook Integration
```python
import requests

def handle_new_lead(lead_data):
    """Called when new lead enters CRM"""
    
    response = requests.post(
        "https://your-agent-service.onrender.com/agent/chat",
        headers={
            "Authorization": "Bearer your_api_key",
            "Content-Type": "application/json"
        },
        json={
            "message": f"New lead: {lead_data['name']} from {lead_data['company']}. Please qualify and suggest next actions.",
            "user_id": lead_data["assigned_sales_rep"],
            "context": lead_data
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        # Update CRM with AI recommendations
        update_lead_notes(lead_data["id"], result["response"])
        schedule_follow_up(lead_data["id"], result["metadata"]["next_actions"])
```

### Real-time Chat Integration
```javascript
// CRM Dashboard Integration
async function askAIAgent(message, context) {
    const response = await fetch('/api/agent/chat', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer your_api_key',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            user_id: getCurrentUserId(),
            context: context
        })
    });
    
    const result = await response.json();
    return result.response;
}

// Usage in CRM
const aiSuggestion = await askAIAgent(
    "How should I follow up with this customer?",
    { customer_id: "123", last_interaction: "demo_completed" }
);
```

## Security Best Practices

1. **Use HTTPS**: Always use SSL/TLS in production
2. **Secure API Keys**: Store API keys in environment variables, never in code
3. **Rotate Keys**: Regularly rotate API keys
4. **CORS Configuration**: Set specific domains in `CORS_ORIGINS`
5. **Rate Limiting**: Implement rate limiting on your CRM side if needed

## Environment Setup for CRM Integration

```bash
# In your Render environment variables
API_KEY=crm_integration_key_xyz789
REQUIRE_API_KEY=true
CORS_ORIGINS=https://your-crm-domain.com,https://app.your-crm.com
```

## Error Handling

```python
def call_ai_agent(message, context):
    try:
        response = requests.post(
            "https://your-agent-service.onrender.com/agent/chat",
            headers={"Authorization": "Bearer your_api_key"},
            json={"message": message, "context": context},
            timeout=30
        )
        
        if response.status_code == 401:
            return {"error": "Invalid API key"}
        elif response.status_code == 503:
            return {"error": "AI Agent temporarily unavailable"}
        elif response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Unexpected error: {response.status_code}"}
            
    except requests.exceptions.Timeout:
        return {"error": "AI Agent response timeout"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to AI Agent service"}
```

## Testing Your Integration

1. **Test without API key** (development):
   ```bash
   curl -X POST "https://your-agent-service.onrender.com/agent/chat" \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello", "user_id": "test"}'
   ```

2. **Test with API key** (production):
   ```bash
   curl -X POST "https://your-agent-service.onrender.com/agent/chat" \
        -H "Authorization: Bearer your_api_key" \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello", "user_id": "test"}'
   ```

## Support and Troubleshooting

- **503 Service Unavailable**: AI agent initialization failed - check logs
- **401 Unauthorized**: Invalid or missing API key
- **422 Validation Error**: Request body format incorrect
- **CORS Error**: Add your domain to `CORS_ORIGINS` environment variable

For more details, visit the API documentation at: `https://your-agent-service.onrender.com/docs`
