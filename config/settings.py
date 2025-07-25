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
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Security Configuration
    SECRET_KEY: str = "your_secret_key_for_production"
    CORS_ORIGINS: str = "*"
    
    # API Security
    API_KEY: Optional[str] = None
    REQUIRE_API_KEY: bool = False
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return not self.DEVELOPMENT_MODE and not self.DEBUG
    
    @property
    def cors_origins_list(self) -> list:
        """Get CORS origins as a list"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    # External Platform Configuration
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    WHATSAPP_API_TOKEN: Optional[str] = None
    WHATSAPP_VERIFY_TOKEN: Optional[str] = None
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
    LOG_TO_FILE: bool = False
    
    # Development Settings
    DEVELOPMENT_MODE: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        # Allow extra fields from .env file
        extra = "allow"


# Global settings instance
settings = Settings()
