# 📁 Project Structure Documentation

## 🏗️ **Organized Folder Structure**

```
AGENT/
├── 📁 api/                     # API Layer
│   ├── main.py                # FastAPI application
│   ├── routes/                # Modular API routes
│   │   ├── agent.py          # Core agent endpoints
│   │   ├── webhooks.py       # External platform webhooks
│   │   └── workflows.py      # Workflow automation
│   ├── schemas/               # Pydantic data models
│   │   ├── requests.py       # Request schemas
│   │   └── responses.py      # Response schemas
│   └── middleware/            # Custom middleware (future)
│
├── 📁 core/                   # Core Business Logic
│   ├── agents/               # Specialized AI agents
│   │   ├── sales_agent.py    # Sales automation
│   │   ├── operations_agent.py # Operations management
│   │   ├── quote_agent.py    # Quote generation
│   │   └── scheduler_agent.py # Meeting scheduling
│   └── engine/               # Core agent engine
│       └── core_agent.py     # Main orchestrator
│
├── 📁 integrations/          # External Platform Integrations
│   ├── whatsapp_integration.py # WhatsApp Business API
│   ├── telegram_integration.py # Telegram Bot API
│   └── web_chat_integration.py # Web chat widget
│
├── 📁 tools/                 # Agent Tools & Utilities
│   ├── crm_tools.py         # CRM system integration
│   ├── sales_tools.py       # Sales-specific tools
│   ├── operations_tools.py  # Operations tools
│   ├── quote_tools.py       # Quote generation tools
│   ├── scheduler_tools.py   # Scheduling tools
│   └── agent_tools.py       # Cross-agent communication
│
├── 📁 workflows/             # Workflow Automation
│   ├── automation.py        # Workflow engine
│   └── examples.py          # Example workflows
│
├── 📁 config/                # Configuration Management
│   └── settings.py          # Application settings
│
├── 📁 tests/                 # Test Suite
│   └── test_basic.py        # Basic functionality tests
│
├── 📁 docs/                  # Documentation
│   └── structure.md         # This file
│
├── 📁 scripts/               # Utility Scripts
│   ├── start.sh             # Linux startup script
│   └── start.bat            # Windows startup script
│
├── 📁 deployment/            # Deployment Configuration
│   ├── Dockerfile           # Docker container setup
│   └── docker-compose.yml   # Multi-container orchestration
│
├── 📁 examples/              # Example Usage
│   └── demo.py              # System demonstration
│
└── 📄 Configuration Files
    ├── .env                 # Environment variables
    ├── .env.example        # Environment template
    ├── requirements.txt     # Python dependencies
    └── README.md           # Project documentation
```

## 🎯 **Benefits of This Structure**

### **1. Separation of Concerns**
- **API Layer** (`api/`): HTTP endpoints and request handling
- **Business Logic** (`core/`): Agent intelligence and orchestration  
- **External Systems** (`integrations/`): Platform-specific code
- **Tools** (`tools/`): Reusable agent capabilities
- **Configuration** (`config/`): Centralized settings

### **2. Modular Architecture**
- Each component is self-contained and replaceable
- Clear dependencies and interfaces
- Easy to test individual components
- Scalable for team development

### **3. Easy Navigation**
- Logical grouping of related files
- Consistent naming conventions
- Clear separation of concerns
- Intuitive folder hierarchy

### **4. Development Workflow**
- **API Development**: Work in `api/` folder
- **Agent Logic**: Modify `core/` components
- **Integration**: Update `integrations/`
- **Tools**: Extend `tools/` capabilities
- **Deployment**: Use `deployment/` configs

## 🚀 **Getting Started**

1. **API Endpoints**: Start with `api/main.py`
2. **Core Logic**: Understand `core/engine/core_agent.py`
3. **Integrations**: Explore platform connections in `integrations/`
4. **Tools**: See available capabilities in `tools/`
5. **Configuration**: Set up `config/settings.py`

## 📖 **Key Files**

| File | Purpose |
|------|---------|
| `api/main.py` | Main FastAPI application |
| `core/engine/core_agent.py` | Core AI agent orchestrator |
| `integrations/*.py` | External platform connections |
| `tools/*.py` | Agent tools and capabilities |
| `config/settings.py` | Application configuration |
| `workflows/automation.py` | Workflow automation engine |

This structure makes the AI Agent system **professional, maintainable, and scalable**! 🎉
