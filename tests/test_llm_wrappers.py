# tests/test_llm_wrappers.py
import pytest
from src.llms.gemini import GeminiLLMProvider
from src.llms.ollama import OllamaLLMProvider
from src.llms.kimi import KimiLLMProvider
from src.llms.mistral import MistralLLMProvider
from src.llms.provider import LLMProvider

@pytest.mark.parametrize("provider_class, expected_response_prefix", [
    (GeminiLLMProvider, "Gemini response to:"),
    (OllamaLLMProvider, "Ollama response to:"),
    (KimiLLMProvider, "Kimi response to:"),
    (MistralLLMProvider, "Mistral response to:"),
])
def test_llm_provider_wrappers(provider_class, expected_response_prefix):
    """Test that each LLM wrapper correctly implements the LLMProvider interface
    and returns a mock response with the expected prefix."""
    provider = provider_class()
    assert isinstance(provider, LLMProvider)

    prompt = "Test prompt"
    response = provider.generate(prompt)
    assert response.startswith(expected_response_prefix)
    assert prompt in response
