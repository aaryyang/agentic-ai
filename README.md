# 🤖 AI Agent CRM System

A sophisticated multi-agent AI system for CRM automation with beautiful web interface and external platform integrations. Built with FastAPI, LangChain, and modern web technologies.

![AI Agent CRM](https://img.shields.io/badge/AI-Agent%20CRM-blue?style=for-the-badge&logo=robot)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)

## ✨ Key Features

### 🤖 Multi-Agent Architecture
- **Core Agent**: Intelligent orchestrator for complex business tasks
- **Sales Agent**: Lead qualification, pipeline management, deal analysis
- **Operations Agent**: Process automation, workflow optimization
- **Quote Agent**: Dynamic pricing, proposal generation
- **Scheduler Agent**: Meeting coordination, follow-up automation

### 🌐 Beautiful Web Interface
- **Modern Landing Page**: Professional showcase with dark theme
- **Interactive Dashboard**: Real-time chat with AI agents
- **Custom Documentation**: Branded API docs with examples
- **Responsive Design**: Perfect on desktop and mobile

### 🔌 Platform Integrations
- **WhatsApp Business API**: Complete webhook and message processing
- **Telegram Bot**: Full bot integration with commands
- **Web Chat Widget**: Embeddable chat for websites
- **RESTful API**: Easy integration with existing systems

### ⚡ Advanced Capabilities
- **Workflow Automation**: Create complex business processes
- **Real-time Processing**: Async operations for performance
- **Structured Logging**: Comprehensive monitoring and debugging
- **Error Handling**: Graceful degradation and recovery

## 🏗️ Project Structure

```
AI-AGENT/
├── 🌐 FRONTEND
│   └── static/                    # Web interface
│       ├── index.html            # Beautiful landing page
│       ├── dashboard.html        # Interactive chat interface
│       ├── docs.html             # Custom documentation
│       └── api.html              # API information page
│
├── 🔧 BACKEND API
│   └── api/                      # FastAPI application
│       ├── main.py               # Application entry point
│       ├── routes/               # API endpoints
│       │   ├── agent.py          # Core agent interactions
│       │   ├── webhooks.py       # External platform webhooks
│       │   ├── workflows.py      # Process automation
│       │   └── testing.py        # Development dashboard
│       └── schemas/              # Request/response models
│           ├── requests.py       # API request schemas
│           └── responses.py      # API response schemas
│
├── 🤖 AI AGENTS
│   └── core/                     # Agent system
│       ├── engine/               # Core AI orchestration
│       │   └── core_agent.py     # Main agent controller
│       └── agents/               # Specialized agents
│           ├── sales_agent.py    # Sales automation
│           ├── operations_agent.py # Process optimization
│           ├── quote_agent.py    # Pricing and quotes
│           └── scheduler_agent.py # Meeting scheduling
│
├── 🛠️ TOOLS & INTEGRATIONS
│   ├── tools/                    # Agent capabilities
│   │   ├── base_tool.py          # Tool foundation
│   │   ├── agent_tools.py        # Agent delegation
│   │   ├── crm_tools.py          # CRM integration
│   │   ├── sales_tools.py        # Sales operations
│   │   ├── operations_tools.py   # Process tools
│   │   ├── quote_tools.py        # Pricing tools
│   │   └── scheduler_tools.py    # Calendar tools
│   │
│   ├── integrations/             # External platforms
│   │   ├── whatsapp_integration.py # WhatsApp Business
│   │   ├── telegram_integration.py # Telegram Bot
│   │   └── web_chat_integration.py # Web Chat
│   │
│   └── workflows/                # Process automation
│       ├── base_workflow.py      # Workflow foundation
│       ├── automation.py         # Automation engine
│       └── examples.py           # Workflow templates
│
├── ⚙️ CONFIGURATION
│   ├── config/                   # Application settings
│   │   └── settings.py           # Environment configuration
│   ├── scripts/                  # Utility scripts
│   │   ├── start.py              # Server launcher
│   │   └── interactive_chat.py   # Terminal chat
│   └── .github/                  # GitHub configuration
│       └── copilot-instructions.md # AI assistant guidelines
│
└── 📦 PROJECT FILES
    ├── .env                      # Environment variables
    ├── .gitignore               # Git ignore rules
    ├── requirements.txt         # Python dependencies
    ├── package.json             # Node.js scripts
    └── README.md                # This file
```

##  Quick Start

### Prerequisites
- **Python 3.11+** (tested with Python 3.13)
- **Groq API Key** ([Get one here](https://console.groq.com))
- **Git** for version control

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AGENT
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env with your API keys
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
   ```

5. **Start the application**
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

6. **Access the interface**
   - **Landing Page**: http://localhost:8000
   - **Dashboard**: http://localhost:8000/dashboard
   - **Documentation**: http://localhost:8000/docs-custom
   - **API Info**: http://localhost:8000/api

## 🎯 Usage Examples

### Web Interface
The easiest way to interact with the AI agents is through the beautiful web dashboard:

1. Navigate to http://localhost:8000
2. Click "Try Dashboard" to access the chat interface
3. Start chatting with the AI agents for various tasks

### API Integration

#### Basic Agent Chat
```python
import requests

response = requests.post("http://localhost:8000/agent/chat", json={
    "message": "Qualify this lead: John Doe from Acme Corp, $50k budget",
    "user_id": "user_123"
})

print(response.json())
```

#### Delegate to Specialist
```python
response = requests.post("http://localhost:8000/agent/delegate", json={
    "agent_type": "sales",
    "task": "Update deal ABC123 to proposal stage with 75% probability",
    "context": {"deal_id": "ABC123"}
})
```

#### Web Chat Integration
```python
response = requests.post("http://localhost:8000/webchat/message", json={
    "session_id": "session_123",
    "message": "I need a quote for CRM integration",
    "user_info": {"name": "John", "email": "john@example.com"}
})
```

### Terminal Chat
For developers who prefer command-line interaction:

```bash
python scripts/interactive_chat.py
```

## � API Documentation

Once running, explore the comprehensive API documentation:

- **🎨 Custom Docs**: http://localhost:8000/docs-custom (Beautiful, branded)
- **🔧 Swagger UI**: http://localhost:8000/docs (Interactive testing)
- **📖 ReDoc**: http://localhost:8000/redoc (Clean reference)
- **💬 Live Demo**: http://localhost:8000/dashboard (Try the agents)

### Core Endpoints

#### Agent Interaction
- `POST /agent/chat` - Direct agent conversation
- `POST /agent/delegate` - Delegate to specialist agents
- `GET /agent/status` - System health check

#### External Platform Webhooks
- `POST /whatsapp/webhook` - WhatsApp Business API
- `POST /telegram/webhook` - Telegram Bot API
- `POST /webchat/message` - Web chat processing

#### Workflow Management
- `POST /workflows/create` - Create automation workflows
- `POST /workflows/{id}/execute` - Execute workflows
- `GET /workflows/` - List available workflows

## � Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API key for LLM access | Yes | - |
| `GROQ_MODEL` | Groq model to use | No | `meta-llama/llama-4-scout-17b-16e-instruct` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token | No | - |
| `WHATSAPP_API_TOKEN` | WhatsApp Business API token | No | - |
| `DEFAULT_AGENT_TEMPERATURE` | LLM temperature setting | No | `0.7` |
| `MAX_TOKENS` | Maximum tokens per response | No | `1000` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

### Agent Configuration

The system uses intelligent defaults and can be customized through environment variables or the `config/settings.py` file.

## 🛠️ Development

### Running in Development Mode
```bash
# With auto-reload
uvicorn api.main:app --reload --port 8000

# With custom host/port
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```

### Using NPM Scripts
```bash
# Install npm dependencies (optional)
npm install

# Start development server
npm run dev

# Start production server
npm run start
```

### Interactive Terminal Chat
```bash
python scripts/interactive_chat.py
```

## 🚀 Production Deployment

### Basic Production Setup
```bash
# Install production dependencies
pip install -r requirements.txt

# Start with multiple workers
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Or use Gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Environment Configuration
1. Set production environment variables
2. Configure proper CORS settings
3. Set up SSL certificates for webhooks
4. Configure rate limiting
5. Set up monitoring and logging

## 🔐 Security Best Practices

- **API Key Management**: Store sensitive keys in environment variables
- **Input Validation**: All requests validated with Pydantic models
- **Error Handling**: Graceful error handling without data exposure
- **Rate Limiting**: Implement for production deployments
- **CORS Configuration**: Properly configure for your domain

## 🎨 Customization

### Theming
The web interface uses a beautiful dark theme with:
- Glass morphism effects
- Smooth animations and transitions
- Responsive design for all devices
- Professional color scheme

### Adding New Agents
1. Create new agent in `core/agents/`
2. Add corresponding tools in `tools/`
3. Update routing in `api/routes/agent.py`
4. Add documentation to custom docs

### Custom Workflows
Create automated business processes in `workflows/examples.py` and execute them via the API.

## 🛟 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**: Check your `.env` file configuration
   ```bash
   # Verify environment variables
   echo $GROQ_API_KEY
   ```

3. **Port Conflicts**: Use a different port
   ```bash
   uvicorn api.main:app --port 8080
   ```

4. **Permission Errors**: Ensure proper file permissions
   ```bash
   chmod +x scripts/start.py
   ```

## 🎯 Features in Detail

### Multi-Agent System
- **Intelligent Routing**: Automatically determines the best agent for each task
- **Context Preservation**: Maintains conversation context across agent interactions
- **Specialized Expertise**: Each agent optimized for specific business functions

### Beautiful Web Interface
- **Modern Design**: Professional dark theme with glass effects
- **Real-time Chat**: Instant responses with typing indicators
- **Responsive Layout**: Perfect experience on all devices
- **Branded Documentation**: Custom docs matching your brand

### Platform Integrations
- **WhatsApp Business**: Complete webhook handling and message processing
- **Telegram Bot**: Full bot functionality with commands and callbacks
- **Web Chat**: Embeddable widget for websites
- **RESTful API**: Easy integration with existing systems

## 📈 Performance

- **Async Processing**: Non-blocking operations for optimal performance
- **Efficient Routing**: Smart request routing to appropriate agents
- **Memory Management**: Optimized conversation memory handling
- **Caching**: Intelligent caching for frequently accessed data

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain Team** for the excellent AI framework
- **FastAPI Team** for the robust web framework
- **Groq** for powerful language model APIs
- **OpenAI** for advancing AI capabilities

---

**🎉 Built with ❤️ for the future of AI-powered business automation**

For more information, visit our [documentation](http://localhost:8000/docs-custom) or try the [live dashboard](http://localhost:8000/dashboard).
