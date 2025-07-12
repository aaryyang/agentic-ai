"""
Main FastAPI application for the AI Agent system
Organized with modular routes and clean architecture
"""

import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import structlog
import os

# Import route modules
from .routes.agent import router as agent_router
from .routes.webhooks import router as webhook_router
from .routes.workflows import router as workflow_router
from .routes.testing import testing_router

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
app.include_router(agent_router, prefix="/agent", tags=["agent"])
app.include_router(webhook_router, prefix="/webhooks", tags=["webhooks"])
app.include_router(workflow_router, prefix="/workflows", tags=["workflows"])
app.include_router(testing_router, tags=["testing"])

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

# Mount static files
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def landing_page():
    """Serve the landing page"""
    static_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    else:
        # Fallback to API response if static file doesn't exist
        return {
            "message": "AI Agent CRM System",
            "version": "2.0.0",
            "docs": "/docs",
            "dashboard": "/dashboard",
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


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AI Agent system is running",
        "version": "2.0.0"
    }


@app.get("/api")
async def api_info():
    """Serve the API information page"""
    static_file = os.path.join(STATIC_DIR, "api.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    else:
        # Fallback to API response if static file doesn't exist
        return {
            "message": "AI Agent CRM System API",
            "version": "2.0.0",
            "docs": "/docs",
            "dashboard": "/dashboard",
            "health": "/health",
            "endpoints": {
                "agent": "/agent",
                "webhooks": "/webhooks", 
                "workflows": "/workflows"
            },
            "features": [
                "Multi-agent AI architecture",
                "WhatsApp Business integration",
                "Telegram bot integration", 
                "Web chat widget",
                "Workflow automation",
                "CRM process automation"
            ]
        }


@app.get("/docs-custom")
async def docs_custom():
    """Serve the custom documentation page"""
    static_file = os.path.join(STATIC_DIR, "docs.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    else:
        # Fallback to redirect to standard docs
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
