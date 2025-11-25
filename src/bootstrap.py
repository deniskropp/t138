# src/bootstrap.py
"""Initializes and configures the entire system."""
import logging
from src.config import settings
from src.paths import get_root_dir, ensure_dir
from src.logger import setup_logging
from src.llms.client import llm_client
from src.agents.registry import agent_registry
from src.session_manager import session_manager
from src.workflow.state import workflow_state_machine

def bootstrap_system():
    """Performs the full system bootstrap sequence."""
    logging.info("Starting system bootstrap...")

    # 1. Config
    _ = settings.APP_NAME # Accessing to ensure config is loaded

    # 2. Path Management
    ensure_dir(get_root_dir())
    ensure_dir(f"{get_root_dir()}/logs")
    ensure_dir(f"{get_root_dir()}/artifacts")
    ensure_dir(f"{get_root_dir()}/prompts")
    ensure_dir(f"{get_root_dir()}/agents/specs") # Ensure agent specs directory exists

    # 3. Logging
    setup_logging()
    logging.info("Logging configured.")

    # 4. LLM Client Initialization
    llm_client._initialize_providers() # Explicitly initialize
    logging.info("LLM client initialized.")

    # 5. Agents (registry) - Load specs
    agent_registry._load_initial_agent_specs()
    logging.info("Agent registry loaded with specifications.")

    # 6. Session Management
    session_manager.start_session()
    logging.info("Session manager initialized.")

    logging.info("System bootstrap complete.")
