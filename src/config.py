# src/config.py
"""Application configuration management."""
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from typing import Optional, Dict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    APP_NAME: str = "AgentFramework"
    LOG_LEVEL: str = "INFO"
    PROMPTS_DIR: str = "prompts"
    ARTIFACTS_DIR: str = "artifacts"

    # LLM Settings
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_ENDPOINT: str = "https://api.gemini.com/v1"

    OLLAMA_HOST: str = "http://localhost:11434"

    KIMI_API_KEY: Optional[str] = None
    KIMI_ENDPOINT: str = "https://api.kimi.ai/v1"

    MISTRAL_API_KEY: Optional[str] = None
    MISTRAL_ENDPOINT: str = "https://api.mistral.ai/v1"

    # Active LLM Providers (comma-separated list of names like "gemini", "ollama")
    ACTIVE_LLM_PROVIDERS: str = "gemini" 

settings = Settings()
