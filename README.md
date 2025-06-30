# AI Agent System - Multi-Agent CRM Automation

A sophisticated LangChain-based multi-agent AI system for CRM automation with external platform integrations. This production-ready system focuses on maximizing process automation via AI Agent workflows and enables external assistant integrations via WhatsApp, web chat, and Telegram.

## ✨ Key Features

### 🤖 Core Agent System
- **Multi-Agent Architecture**: Specialized agents for sales, operations, quotes, and scheduling
- **LangChain Integration**: Built on LangChain framework for robust agent orchestration
- **Process Automation**: Comprehensive workflow automation capabilities
- **Memory Management**: Conversation memory and context retention
- **API-First Design**: RESTful API for maximum integration flexibility

### 🎯 Specialized Agents
- **Sales Agent**: Lead qualification, pipeline management, deal analysis
- **Operations Agent**: Process automation, workflow optimization, task management
- **Quote Agent**: Pricing calculations, quote generation, proposal creation
- **Scheduler Agent**: Meeting scheduling, calendar management, follow-ups

### 🌐 External Platform Integrations
- **WhatsApp Business API**: Complete webhook handling and message processing
- **Telegram Bot**: Full bot integration with command and callback support
- **Web Chat**: Embeddable chat widget with session management
- **Real-time Processing**: Async processing for optimal performance

### ⚡ Workflow Automation
- **Modular Workflows**: Create complex automated business processes
- **Multiple Trigger Types**: Manual, scheduled, event-based, and webhook triggers
- **Flexible Step Types**: Agent tasks, CRM updates, notifications, conditions, loops
- **Execution Monitoring**: Real-time workflow execution tracking and logging

## 🏗️ Project Structure

```
AGENT/
├── api/                      # FastAPI application and routes
│   ├── main.py              # FastAPI app initialization
│   └── routes/              # API route definitions
│       └── agent.py         # Agent interaction endpoints
├── core/                    # Core AI agent engine
│   └── engine/
│       └── core_agent.py    # Main AI Agent orchestrator
├── integrations/            # External platform integrations
│   ├── whatsapp_integration.py  # WhatsApp Business API
│   ├── telegram_integration.py  # Telegram Bot API
│   └── web_chat_integration.py  # Web chat integration
├── tools/                   # Agent tools and utilities
│   ├── base_tool.py         # Base tool interface
│   ├── agent_tools.py       # Agent delegation tools
│   ├── crm_tools.py         # CRM integration tools
│   ├── sales_tools.py       # Sales-specific tools
│   ├── operations_tools.py  # Operations tools
│   ├── quote_tools.py       # Quote generation tools
│   └── scheduler_tools.py   # Scheduling tools
├── workflows/               # Business workflow automation
│   ├── base_workflow.py     # Base workflow interface
│   ├── automation.py        # Workflow automation engine
│   └── examples.py          # Example workflow configurations
├── config/                  # Configuration management
│   └── settings.py          # Application settings
├── tests/                   # Test suite
├── examples/                # Usage examples and demos
├── scripts/                 # Utility scripts
├── deployment/              # Deployment configurations
└── docs/                    # Documentation
## 🛠️ Technology Stack

- **AI Framework**: LangChain, OpenAI GPT-4
- **Web Framework**: FastAPI, Uvicorn
- **Data Validation**: Pydantic
- **Logging**: Structlog
- **Async Processing**: Python asyncio
- **Type Safety**: Python type hints throughout

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (tested with Python 3.13.2)
- OpenAI API key
- Git (for version control)

### Installation

1. **Clone and setup:**
```bash
git clone <repository-url>
cd AGENT
cp .env.example .env
```

2. **Configure environment variables:**
```bash
# Edit .env file with your API keys
OPENAI_API_KEY=your_openai_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token  # Optional
WHATSAPP_API_TOKEN=your_whatsapp_api_token  # Optional
```

3. **Install dependencies:**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

4. **Run the application:**
```bash
# Start the AI Agent system
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Verification

```bash
# Test imports and system health
python -c "
from api.routes.agent import router
from core.engine.core_agent import CoreAIAgent
from integrations.whatsapp_integration import WhatsAppIntegration
print('✅ All systems operational!')
"
```

## 📚 API Documentation

Once running, visit:
- **API Documentation**: http://localhost:8000/docs
- **API Schema**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

### Core Endpoints

#### Agent Interaction
```bash
POST /agent/chat           # Direct agent interaction
POST /agent/delegate       # Delegate to specialist agents
GET /agent/status          # Agent system status
```

#### External Platform Webhooks
```bash
# WhatsApp
GET /whatsapp/webhook      # Webhook verification
POST /whatsapp/webhook     # Message handling

# Telegram
POST /telegram/webhook     # Update handling

# Web Chat
POST /webchat/message      # Message processing
POST /webchat/session      # Session management
```

#### Workflow Management
```bash
POST /workflows/automate   # Set up process automation
POST /sales/qualify-lead   # Automated lead qualification
POST /quotes/generate      # Quote generation
POST /schedule/meeting     # Meeting scheduling
```

## 🤖 Usage Examples

### 1. Direct Agent Interaction

```python
import requests

# Chat with the core agent
response = requests.post("http://localhost:8000/agent/chat", json={
    "message": "Qualify this lead: John Doe from Acme Corp, $50k budget, needs CRM solution",
    "user_id": "user_123",
    "context": {"source": "web_form"}
})

print(response.json())
```

### 2. Delegate to Specialist Agent

```python
# Delegate to sales agent
response = requests.post("http://localhost:8000/agent/delegate", json={
    "agent_type": "sales",
    "task": "Update deal ABC123 to proposal stage with 75% probability",
    "context": {"deal_id": "ABC123"}
})
```

### 3. WhatsApp Integration

```python
# Example webhook payload from WhatsApp
webhook_data = {
    "entry": [{
        "changes": [{
            "value": {
                "messages": [{
                    "from": "1234567890",
                    "text": {"body": "I need help with pricing"},
                    "type": "text"
                }]
            }
        }]
    }]
}

# This would be sent by WhatsApp to your webhook endpoint
# POST /whatsapp/webhook
```

### 4. Web Chat Integration

```python
# Start a chat session
response = requests.post("http://localhost:8000/webchat/session", json={
    "session_id": "session_123",
    "user_info": {"name": "John", "email": "john@example.com"}
})

# Send a message
response = requests.post("http://localhost:8000/webchat/message", json={
    "session_id": "session_123",
    "message": "I need a quote for CRM integration",
    "user_info": {"name": "John"}
})
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM access | Yes | - |
| `OPENAI_MODEL` | OpenAI model to use | No | `gpt-4o-mini` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | No | - |
| `WHATSAPP_API_TOKEN` | WhatsApp Business API token | No | - |
| `DEFAULT_AGENT_TEMPERATURE` | LLM temperature setting | No | `0.7` |
| `MAX_TOKENS` | Maximum tokens per response | No | `1000` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

### Agent Configuration

The system uses intelligent defaults and can be customized through environment variables or the `config/settings.py` file.

## 🔄 Development Workflow

### Setting up for Development

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd AGENT

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
cp .env.example .env

# 5. Edit .env with your API keys
# OPENAI_API_KEY=your_key_here

# 6. Run the application
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_basic.py

# Run with coverage
python -m pytest tests/ --cov=.
```

### Code Quality

```bash
# Check imports and basic syntax
python -c "
from api.routes.agent import router
from core.engine.core_agent import CoreAIAgent
print('✅ All imports working correctly')
"
```

## 🧪 Testing

The system includes comprehensive tests to ensure reliability:

```bash
# Run all tests
python -m pytest tests/

# Run basic functionality tests
python -m pytest tests/test_basic.py

# Test imports and core functionality
python examples/demo.py

# Test API endpoints (with server running)
python examples/usage_examples.py
```

## 📊 System Status

### Health Monitoring
- **Application Health**: Automatic system health checks
- **Agent Status**: Real-time agent availability monitoring
- **Integration Status**: External platform connection monitoring

### Logging
- **Structured Logging**: JSON-formatted logs via structlog
- **Request Tracking**: Full request/response cycle logging
- **Error Monitoring**: Comprehensive error tracking and reporting

## 🔐 Security Best Practices

- **API Key Management**: Secure environment variable handling
- **Input Validation**: Pydantic models for data validation
- **Error Handling**: Graceful error handling without data exposure
- **Environment Isolation**: Separate development and production configs

## 📈 Deployment

### Local Development
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment
```bash
# Using Uvicorn with production settings
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or using Gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Environment Setup
1. Clone repository
2. Set up virtual environment
3. Install dependencies
4. Configure environment variables
5. Run application

## �️ Roadmap

### Current Status: ✅ Production Ready
- ✅ Multi-agent architecture implemented
- ✅ External platform integrations (WhatsApp, Telegram, Web Chat)
- ✅ API-first design with FastAPI
- ✅ Comprehensive workflow automation
- ✅ Production-ready error handling and logging

### Phase 3 (Planned)
- **RAG Integration**: Retrieval-Augmented Generation for knowledge base
- **Vector Database**: Semantic search capabilities
- **Advanced Memory**: Long-term conversation memory
- **Multi-tenant Support**: SaaS-ready architecture

### Phase 4 (Future)
- **Voice Integration**: Speech-to-text and text-to-speech
- **Analytics Dashboard**: Real-time performance monitoring
- **Custom Agent Training**: Domain-specific agent customization
- **Enterprise Features**: Advanced security and compliance

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` endpoint when running
- **Issues**: Open GitHub issues for bugs and feature requests
- **Community**: Join our Discord/Slack for discussions

## 🙏 Acknowledgments

- LangChain team for the excellent framework
- OpenAI for powerful language models
- FastAPI team for the robust web framework
- All contributors and community members

---

**Built with ❤️ for the future of AI-powered business automation**
