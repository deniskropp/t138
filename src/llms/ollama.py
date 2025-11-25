# src/llms/ollama.py
"""LLM wrapper for Ollama models."""
from src.llms.provider import LLMProvider
import logging

logger = logging.getLogger(__name__)

class OllamaLLMProvider(LLMProvider):
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host

    def generate(self, prompt: str) -> str:
        """Generates a response using the Ollama LLM."""
        # Placeholder for actual API call using self.host
        return f"Ollama response from {self.host} for: {prompt}" # Placeholder
