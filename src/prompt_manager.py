# src/prompt_manager.py
"""Manages loading and retrieval of prompt templates."""
import os
from typing import Dict
from src.file_io import read_file
from src.paths import get_root_dir, ensure_dir
from src.config import settings
import logging

logger = logging.getLogger(__name__)

class PromptManager:
    def __init__(self, prompt_dir: str = None):
        self.prompt_dir = os.path.join(get_root_dir(), prompt_dir or settings.PROMPTS_DIR)
        ensure_dir(self.prompt_dir)
        self.prompts: Dict[str, str] = {}
        self.load_prompts()

    def load_prompts(self):
        """Loads prompt templates from the specified directory."""
        self.prompts = {}
        for filename in os.listdir(self.prompt_dir):
            if filename.endswith(".txt"):
                name = os.path.splitext(filename)[0]
                filepath = os.path.join(self.prompt_dir, filename)
                content = read_file(filepath)
                if content is not None:
                    self.prompts[name] = content
                    logger.info(f"Loaded prompt: {name}")
                else:
                    logger.warning(f"Could not load prompt from {filepath}")

    def get_prompt(self, name: str) -> str:
        """Retrieves a prompt template by name."""
        return self.prompts.get(name, "")

    def update_prompt(self, name: str, new_content: str):
        """Updates an existing prompt template in memory."""
        self.prompts[name] = new_content
        logger.info(f"Updated prompt '{name}' in memory.")

prompt_manager = PromptManager()
