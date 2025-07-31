"""Configuration management for NLyzer platform.

This module provides centralized configuration management using Pydantic's BaseSettings.
All configuration values are loaded from environment variables or a .env file,
ensuring secure handling of secrets and easy deployment across environments.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file.
    
    This class defines all configuration parameters for the NLyzer platform,
    including security settings, database connections, and API keys. Values
    are automatically loaded from environment variables or a .env file.
    
    Attributes:
        SECRET_KEY: Secret key for JWT token signing and other cryptographic operations.
        ALGORITHM: Algorithm used for JWT token encoding/decoding.
        ACCESS_TOKEN_EXPIRE_MINUTES: JWT token expiration time in minutes.
        DATABASE_URL: PostgreSQL database connection URL.
    """
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    
    class Config:
        """Pydantic configuration for settings loading."""
        env_file = ".env"


# Global settings instance - import this throughout the application
settings = Settings()