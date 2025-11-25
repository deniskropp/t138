# src/runtime.py
"""Central class holding global system state, registries, and core components."""
from src.config import Settings, settings
from src.agents.registry import AgentRegistry, agent_registry
from src.session_manager import SessionManager, session_manager
import logging

class SystemRuntime:
    def __init__(self):
        self.config: Settings = settings
        self.logger = logging.getLogger(__name__)
        self.agent_registry: AgentRegistry = agent_registry
        self.session_manager: SessionManager = session_manager
        # Add other components as they are initialized

system_runtime = SystemRuntime()
