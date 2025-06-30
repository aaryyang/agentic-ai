# 🚀 **AI Agent CRM System v2.0**
## Multi-Agent AI Architecture with Clean Code Organization

[![FastAPI](https://img.shields.io/badge/FastAPI-0.108.0-blue)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3.25-green)](https://langchain.com/)
[![Python](https://img.shields.io/badge/Python-3.13-yellow)](https://python.org/)

> **Production-ready multi-agent AI system for CRM automation with external platform integrations. Now with improved modular architecture!**

---

## 🏗️ **New Organized Structure**

```
📁 AGENT/
├── 🌐 api/              # Clean API layer with modular routes
├── 🧠 core/             # AI agents and business logic  
├── 🔗 integrations/     # WhatsApp, Telegram, Web Chat
├── 🛠️ tools/            # Agent capabilities and utilities
├── ⚡ workflows/        # Process automation engine
├── ⚙️ config/           # Centralized configuration
├── 🧪 tests/            # Comprehensive test suite
├── 📚 docs/             # Complete documentation
├── 🔧 scripts/          # Utility scripts
└── 🚀 deployment/       # Docker & deployment configs
```

## ✨ **What's New in v2.0**

### 🎯 **Improved Architecture**
- **Modular API Routes**: Clean separation of endpoints
- **Structured Core Logic**: Organized agents and engine
- **Better Configuration**: Centralized settings management
- **Enhanced Documentation**: Complete project docs

### 🔧 **Developer Experience**
- **Easy Navigation**: Logical folder hierarchy
- **Clear Dependencies**: Well-defined interfaces
- **Scalable Design**: Ready for team development
- **Professional Structure**: Industry-standard organization

---

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

### **3. Start the System**
```bash
# Using new API structure
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Or using scripts
.\scripts\start.bat  # Windows
./scripts/start.sh   # Linux/Mac
```

### **4. Explore the API**
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **System Info**: http://localhost:8000/

---

## 🎯 **Core Features**

### **🤖 Multi-Agent Architecture**
- **Core Agent**: Orchestrates all operations
- **Sales Agent**: Lead qualification & pipeline management
- **Operations Agent**: Process automation & optimization  
- **Quote Agent**: Pricing calculations & proposal generation
- **Scheduler Agent**: Meeting scheduling & follow-ups

### **🌍 External Platform Integrations**
- **WhatsApp Business API**: Customer support via WhatsApp
- **Telegram Bot API**: Automated bot interactions
- **Web Chat Widget**: Embeddable website chat

### **⚡ Workflow Automation**
- **Process Automation**: Streamline business workflows
- **Task Management**: Automated task execution
- **Custom Workflows**: Build your own automation

### **🛠️ Agent Tools & Capabilities**
- **CRM Integration**: Direct CRM system access
- **Cross-Agent Communication**: Seamless agent collaboration
- **Data Management**: Efficient data processing
- **API Integration**: External service connections

---

## 📖 **API Documentation**

### **Core Endpoints**
```http
POST /agent/chat              # Direct agent interaction
POST /agent/delegate          # Delegate to specialized agents
GET  /agent/status            # System status and health
```

### **External Platform Webhooks**
```http
GET/POST /webhooks/whatsapp   # WhatsApp Business API
POST     /webhooks/telegram   # Telegram Bot API
POST     /webchat/message     # Web chat messages
```

### **Workflow Automation**
```http
POST /workflows/create        # Create automation workflow
POST /workflows/{id}/execute  # Execute specific workflow
GET  /workflows              # List all workflows
```

### **Specialized Agent Functions**
```http
POST /sales/qualify-lead      # Automated lead qualification
POST /quotes/generate         # Generate quotes and proposals
POST /schedule/meeting        # Schedule meetings and calls
```

---

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Core Configuration
OPENAI_API_KEY=your_openai_key
ENVIRONMENT=development

# External Platform APIs
WHATSAPP_API_TOKEN=your_whatsapp_token
WHATSAPP_WEBHOOK_TOKEN=your_webhook_token
TELEGRAM_BOT_TOKEN=your_telegram_token

# Infrastructure
REDIS_URL=redis://localhost:6379
```

### **Settings Management**
Configuration is centralized in `config/settings.py` using Pydantic settings for validation and type safety.

---

## 🏗️ **Development Guide**

### **Project Structure Navigation**
- **API Development**: Work in `api/` folder
- **Agent Logic**: Modify `core/` components  
- **Platform Integration**: Update `integrations/`
- **Tool Development**: Extend `tools/` capabilities
- **Workflow Creation**: Build in `workflows/`

### **Key Development Files**
| Component | File | Purpose |
|-----------|------|---------|
| **API** | `api/main.py` | FastAPI application |
| **Core** | `core/engine/core_agent.py` | Main orchestrator |
| **Routes** | `api/routes/*.py` | Modular API endpoints |
| **Schemas** | `api/schemas/*.py` | Request/response models |
| **Config** | `config/settings.py` | Application settings |

### **Adding New Features**
1. **New Agent**: Add to `core/agents/`
2. **New Integration**: Add to `integrations/`
3. **New Tool**: Add to `tools/`
4. **New Endpoint**: Add route to `api/routes/`
5. **New Schema**: Add model to `api/schemas/`

---

## 🚀 **Deployment**

### **Docker Deployment**
```bash
cd deployment/
docker-compose up -d
```

### **Production Setup**
1. **Environment**: Set production environment variables
2. **Security**: Configure CORS and authentication
3. **Monitoring**: Set up logging and health checks
4. **Scaling**: Use multiple worker processes

---

## 🧪 **Testing**

```bash
# Run tests
pytest tests/

# Run specific test
pytest tests/test_basic.py

# Run with coverage
pytest --cov=src tests/
```

---

## 📚 **Documentation**

- **📁 Structure Guide**: `docs/structure.md`
- **🌐 API Reference**: http://localhost:8000/docs
- **🔧 Configuration**: `config/settings.py`
- **💡 Examples**: `examples/demo.py`

---

## 🤝 **Contributing**

1. **Follow Structure**: Use the organized folder hierarchy
2. **Code Style**: Follow Python PEP 8 standards
3. **Documentation**: Update docs for new features
4. **Testing**: Add tests for new functionality

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎉 **Ready to Build Amazing AI Automation!**

The new organized structure makes development faster, code cleaner, and the system more maintainable. Start building your AI-powered CRM automation today! 🚀
