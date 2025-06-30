"""
Main FastAPI application for the AI Agent system
Organized with modular routes and clean architecture
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

# Import route modules
from .routes.agent import router as agent_router
from .routes.webhooks import router as webhook_router
from .routes.workflows import router as workflow_router

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    logger.info("🚀 AI Agent system starting up...")
    
    # Initialize core components
    try:
        logger.info("✅ Core components initialized")
        logger.info("🌐 AI Agent system ready for requests")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 AI Agent system shutting down...")


# Create FastAPI application
app = FastAPI(
    title="AI Agent CRM System",
    description="Multi-agent AI system for CRM automation with external platform integrations",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent_router)
app.include_router(webhook_router)
app.include_router(workflow_router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI Agent system is running",
        "version": "2.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "AI Agent CRM System",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "features": [
            "Multi-agent AI architecture",
            "WhatsApp Business integration",
            "Telegram bot integration", 
            "Web chat widget",
            "Workflow automation",
            "CRM process automation"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
