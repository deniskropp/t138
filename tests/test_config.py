# tests/test_config.py
import pytest
from src.config import settings

def test_config_loading():
    """Test that configuration settings are loaded correctly."""
    assert settings.APP_NAME == "AgentFramework"
    assert settings.LOG_LEVEL == "INFO"
    assert settings.PROMPTS_DIR == "prompts"
    assert settings.ARTIFACTS_DIR == "artifacts"

def test_config_override_with_env_vars(monkeypatch):
    """Test that environment variables can override default settings."""
    monkeypatch.setenv("APP_NAME", "TestApp")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    # Reload settings after patching environment variables
    from src.config import Settings
    reloaded_settings = Settings()
    assert reloaded_settings.APP_NAME == "TestApp"
    assert reloaded_settings.LOG_LEVEL == "DEBUG"
