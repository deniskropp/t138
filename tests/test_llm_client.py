# tests/test_llm_client.py
import pytest
from unittest.mock import patch, MagicMock
from src.llms.client import LLMClient
from src.llms.provider import LLMProvider
from src.config import settings

@pytest.fixture(autouse=True)
def mock_llm_settings(monkeypatch):
    """Mock LLM settings for testing."""
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "dummy_gemini_key")
    monkeypatch.setattr(settings, "GEMINI_ENDPOINT", "http://mock-gemini.com")
    monkeypatch.setattr(settings, "OLLAMA_HOST", "http://mock-ollama.com")
    monkeypatch.setattr(settings, "KIMI_API_KEY", "dummy_kimi_key")
    monkeypatch.setattr(settings, "KIMI_ENDPOINT", "http://mock-kimi.com")
    monkeypatch.setattr(settings, "MISTRAL_API_KEY", "dummy_mistral_key")
    monkeypatch.setattr(settings, "MISTRAL_ENDPOINT", "http://mock-mistral.com")
    monkeypatch.setattr(settings, "ACTIVE_LLM_PROVIDERS", "gemini,ollama,kimi,mistral")

    # Ensure settings are reloaded after monkeypatching
    from src.config import Settings
    monkeypatch.setattr('src.config.settings', Settings())

@pytest.fixture
def clean_llm_client():
    """Provides a fresh LLMClient instance for each test."""
    return LLMClient()

def test_llm_client_initializes_active_providers(clean_llm_client):
    """Test that the LLMClient initializes all active providers."""
    client = clean_llm_client
    assert "gemini" in client.providers
    assert "ollama" in client.providers
    assert "kimi" in client.providers
    assert "mistral" in client.providers

    assert isinstance(client.get_provider("gemini"), LLMProvider)
    assert isinstance(client.get_provider("ollama"), LLMProvider)
    assert isinstance(client.get_provider("kimi"), LLMProvider)
    assert isinstance(client.get_provider("mistral"), LLMProvider)

def test_llm_client_does_not_initialize_inactive_providers(monkeypatch):
    """Test that LLMClient only initializes specified active providers."""
    monkeypatch.setattr(settings, "ACTIVE_LLM_PROVIDERS", "gemini")
    from src.config import Settings
    monkeypatch.setattr('src.config.settings', Settings()) # Reload settings

    client = LLMClient()
    assert "gemini" in client.providers
    assert "ollama" not in client.providers
    assert "kimi" not in client.providers
    assert "mistral" not in client.providers

def test_llm_client_get_provider_returns_correct_instance(clean_llm_client):
    """Test that get_provider returns the correct provider instance."""
    client = clean_llm_client
    gemini_provider = client.get_provider("gemini")
    ollama_provider = client.get_provider("ollama")

    assert gemini_provider is not None
    assert ollama_provider is not None
    assert gemini_provider != ollama_provider

def test_llm_client_get_provider_for_non_existent_provider(clean_llm_client):
    """Test that get_provider returns None for a non-existent provider."""
    client = clean_llm_client
    assert client.get_provider("non_existent") is None

def test_llm_client_handles_missing_api_key(monkeypatch, caplog):
    """Test that LLMClient handles missing API keys gracefully."""
    monkeypatch.setattr(settings, "GEMINI_API_KEY", None)
    monkeypatch.setattr(settings, "KIMI_API_KEY", None)
    monkeypatch.setattr(settings, "MISTRAL_API_KEY", None)
    monkeypatch.setattr(settings, "ACTIVE_LLM_PROVIDERS", "gemini,kimi,mistral")
    from src.config import Settings
    monkeypatch.setattr('src.config.settings', Settings()) # Reload settings

    with caplog.at_level(logging.WARNING):
        client = LLMClient()
        assert "Gemini API key not found." in caplog.text
        assert "Kimi API key not found." in caplog.text
        assert "Mistral API key not found." in caplog.text
        assert "gemini" not in client.providers # Should not be initialized if API key is None
        assert "kimi" not in client.providers
        assert "mistral" not in client.providers
