"""
Authentication utilities for API endpoints
"""

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from config.settings import settings

# Security
security = HTTPBearer(auto_error=False)

async def verify_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)):
    """Verify API key for protected endpoints"""
    # If API key is not required, allow access
    if not settings.REQUIRE_API_KEY:
        return True
    
    # If API key is required but no credentials provided
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="API key required"
        )
    
    api_key = credentials.credentials
    valid_api_key = settings.API_KEY
    
    if not valid_api_key:
        raise HTTPException(
            status_code=500,
            detail="Server configuration error: API key not set"
        )
        
    if api_key != valid_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return True
