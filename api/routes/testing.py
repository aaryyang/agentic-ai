"""
Enhanced dashboard endpoint with modern UI
"""
from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse
import os

testing_router = APIRouter()

@testing_router.get("/dashboard")
async def dashboard():
    """Modern AI Agent Dashboard"""
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dashboard_file = os.path.join(project_root, "static", "dashboard.html")
    
    if os.path.exists(dashboard_file):
        return FileResponse(dashboard_file)
    else:
        # Fallback to basic dashboard if file doesn't exist
        return basic_dashboard()


def basic_dashboard():
    """Fallback basic dashboard"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Agent Dashboard - Fallback</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: #0f172a; 
                color: #f8fafc; 
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: rgba(255, 255, 255, 0.1); 
                padding: 30px; 
                border-radius: 20px; 
                backdrop-filter: blur(20px);
            }
            h1 { 
                color: #6366f1; 
                text-align: center; 
                margin-bottom: 30px; 
            }
            .status { 
                background: rgba(16, 185, 129, 0.1); 
                padding: 15px; 
                margin: 20px 0; 
                border-radius: 10px; 
                border-left: 4px solid #10b981;
            }
            .error { 
                background: rgba(239, 68, 68, 0.1); 
                color: #f87171; 
                padding: 15px; 
                margin: 20px 0; 
                border-radius: 10px; 
                border-left: 4px solid #ef4444;
            }
            a { color: #60a5fa; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Agent Dashboard (Fallback)</h1>
            <div class="error">
                ⚠️ Dashboard files not found. Please ensure static files are properly configured.
            </div>
            <div class="status">
                <strong>Available Endpoints:</strong><br>
                • <a href="/docs">API Documentation</a><br>
                • <a href="/agent/status">Agent Status</a><br>
                • <a href="/health">Health Check</a><br>
                • <a href="/">Home Page</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
