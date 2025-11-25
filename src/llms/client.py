# src/llms/client.py
"""Initializes and manages LLM client instances."""
from typing import Dict, Type, Optional
from src.config import settings
from src.llms.provider import LLMProvider
from src.llms.gemini import GeminiLLMProvider
from src.llms.ollama import OllamaLLMProvider
from src.llms.kimi import KimiLLMProvider
from src.llms.mistral import MistralLLMProvider
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.providers: Dict[str, LLMProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initializes various LLM providers based on configuration."""
        active_providers = [p.strip().lower() for p in settings.ACTIVE_LLM_PROVIDERS.split(',')]

        if "gemini" in active_providers:
            if settings.GEMINI_API_KEY:
                self.providers["gemini"] = GeminiLLMProvider(
                    api_key=settings.GEMINI_API_KEY,
                    endpoint=settings.GEMINI_ENDPOINT
                )
                logger.info("Gemini LLM provider initialized.")
            else:
                logger.warning("Gemini API key not found. Gemini provider not initialized.")

        if "ollama" in active_providers:
            self.providers["ollama"] = OllamaLLMProvider(
                host=settings.OLLAMA_HOST
            )
            logger.info("Ollama LLM provider initialized.")

        if "kimi" in active_providers:
            if settings.KIMI_API_KEY:
                self.providers["kimi"] = KimiLLMProvider(
                    api_key=settings.KIMI_API_KEY,
                    endpoint=settings.KIMI_ENDPOINT
                )
                logger.info("Kimi LLM provider initialized.")
            else:
                logger.warning("Kimi API key not found. Kimi provider not initialized.")
        
        if "mistral" in active_providers:
            if settings.MISTRAL_API_KEY:
                self.providers["mistral"] = MistralLLMProvider(
                    api_key=settings.MISTRAL_API_KEY,
                    endpoint=settings.MISTRAL_ENDPOINT
                )
                logger.info("Mistral LLM provider initialized.")
            else:
                logger.warning("Mistral API key not found. Mistral provider not initialized.")


    def get_provider(self, name: str) -> Optional[LLMProvider]:
        """Returns an initialized LLM provider by name."""
        return self.providers.get(name)

llm_client = LLMClient()
