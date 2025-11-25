# src/llms/provider.py
"""Defines the abstract interface for Large Language Model providers."""
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generates a response from the LLM based on the given prompt."""
        pass
