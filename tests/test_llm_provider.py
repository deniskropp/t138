# tests/test_llm_provider.py
import pytest
from abc import ABC, abstractmethod
from src.llms.provider import LLMProvider

def test_abstract_llm_provider_cannot_be_instantiated():
    """Test that the abstract LLMProvider class cannot be instantiated directly."""
    with pytest.raises(TypeError):
        LLMProvider()

def test_concrete_llm_provider_implementation():
    """Test a concrete implementation of the LLMProvider class."""
    class ConcreteLLMProvider(LLMProvider):
        def generate(self, prompt: str) -> str:
            return f"Response to: {prompt}"

    provider = ConcreteLLMProvider()
    assert provider.generate("Hello") == "Response to: Hello"

def test_concrete_llm_provider_missing_generate_implementation():
    """Test that a concrete provider must implement the generate method."""
    class InvalidLLMProvider(LLMProvider):
        # Missing generate method
        pass

    with pytest.raises(TypeError):
        InvalidLLMProvider()
