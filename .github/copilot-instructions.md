<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# AI Agent System - Copilot Instructions

This is a LangChain-based multi-agent AI system for CRM automation with external platform integrations.

## Project Overview

The system implements a modular, multi-agent architecture focused on:
- **Process automation** via AI Agent workflows
- **External assistant integrations** via WhatsApp, web chat, and Telegram
- **Specialized agents** for sales, operations, quotes, and scheduling
- **API-first design** for maximum integration flexibility

## Key Technologies

- **LangChain** for agent orchestration and tool management
- **FastAPI** for REST API endpoints
- **OpenAI GPT-4** for natural language processing
- **Pydantic** for data validation and serialization
- **Structlog** for structured logging

## Architecture Components

### Core Agent (`src/core/agent.py`)
- Main orchestrator that coordinates specialized agents
- Handles high-level decision making and task delegation
- Manages conversation memory and context

### Specialized Agents (`src/agents/`)
- **SalesAgent**: Lead qualification, pipeline management, deal analysis
- **OperationsAgent**: Process automation, workflow optimization, task management
- **QuoteAgent**: Pricing calculations, quote generation, proposal creation
- **SchedulerAgent**: Meeting scheduling, calendar management, follow-ups

### Tools (`src/tools/`)
- Modular tools for each agent specialization
- CRM integration tools for data access and updates
- Agent delegation tools for cross-agent communication

### External Integrations (`src/integrations/`)
- **WhatsAppIntegration**: Business API integration with webhook handling
- **TelegramIntegration**: Bot API with command and callback support
- **WebChatIntegration**: Embeddable chat widget with session management

## Development Guidelines

### Code Style
- Use async/await for all agent and integration operations
- Implement proper error handling with structured logging
- Follow Pydantic models for data validation
- Use type hints throughout the codebase

### Agent Development
- Each agent should inherit proper LangChain patterns
- Use specialized tools for domain-specific operations
- Implement proper memory management for conversation context
- Include comprehensive error handling and fallbacks

### Integration Development
- All external integrations should handle webhook verification
- Implement proper message queuing for high-volume scenarios
- Use background tasks for non-blocking message processing
- Include retry logic for failed external API calls

### Testing Approach
- Mock external API calls for unit testing
- Use pytest-asyncio for async test functions
- Create integration tests for full workflow scenarios
- Test error conditions and edge cases

## Environment Setup

The system requires these environment variables:
- `OPENAI_API_KEY`: OpenAI API key for LLM access
- `TELEGRAM_BOT_TOKEN`: Telegram bot token (optional)
- `WHATSAPP_API_TOKEN`: WhatsApp Business API token (optional)
- `REDIS_URL`: Redis connection for background tasks
- `CRM_API_KEY`: CRM system integration key

## API Endpoints

### Core Agent
- `POST /agent/chat`: Direct agent interaction
- `POST /agent/delegate`: Delegate to specialist agents
- `GET /agent/status`: Agent system status

### External Platforms
- `POST /whatsapp/webhook`: WhatsApp message handling
- `POST /telegram/webhook`: Telegram update processing
- `POST /webchat/message`: Web chat message processing

### Workflow Automation
- `POST /workflows/automate`: Set up process automation
- `POST /sales/qualify-lead`: Automated lead qualification
- `POST /quotes/generate`: Quote generation
- `POST /schedule/meeting`: Meeting scheduling

## Deployment Considerations

- Use Docker containers for consistent deployment
- Configure proper CORS settings for web chat integration
- Set up webhook endpoints with SSL certificates
- Implement rate limiting for external platform endpoints
- Use environment-specific configuration files

## Future Enhancements

- RAG (Retrieval-Augmented Generation) integration for knowledge base
- Vector database integration for semantic search
- Multi-tenant support for SaaS deployment
- Advanced analytics and reporting capabilities
- Voice integration for phone-based interactions
