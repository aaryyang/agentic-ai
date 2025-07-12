"""
Configuration settings for the AI Agent system
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Groq Configuration (Primary LLM)
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "meta-llama/llama-4-scout-17b-16e-instruct"
    
    # Legacy OpenAI Configuration (Optional fallback)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: Optional[str] = None
    
    # Agent Configuration
    DEFAULT_AGENT_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000
    CONVERSATION_MEMORY_SIZE: int = 20
    GROQ_STREAMING: bool = False
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # External Platform Configuration
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    WHATSAPP_API_TOKEN: Optional[str] = None
    WHATSAPP_WEBHOOK_TOKEN: Optional[str] = None
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CRM Configuration
    CRM_API_BASE_URL: Optional[str] = None
    CRM_API_KEY: Optional[str] = None
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
