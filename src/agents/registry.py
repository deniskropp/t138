# src/agents/registry.py
"""Manages registration and lookup of agent implementations."""
from typing import Dict, Type, Optional, List
from src.agents.base import Agent
from src.models import AgentSpec
from src.agent_loader import load_agent_specs # Import the loader
import logging

# Import concrete agent implementations here
from src.agents.dummy_agent import DummyAgent

logger = logging.getLogger(__name__)

class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, Type[Agent]] = {}
        self._agent_specs: Dict[str, AgentSpec] = {}
        self._load_initial_agent_specs()
        self._register_concrete_agents() # New call

    def _load_initial_agent_specs(self):
        """Loads agent specifications and registers them."""
        specs = load_agent_specs()
        for spec in specs:
            self._agent_specs[spec.name] = spec
            logger.info(f"Registered agent spec for: {spec.name}")

    def _register_concrete_agents(self):
        """Registers concrete agent classes."""
        self.register_agent_class(DummyAgent)
        # Add other concrete agent classes here as they are developed

    def register_agent_class(self, agent_class: Type[Agent]):
        """Registers an agent class with its name."""
        # Use the class name as the key for the agent class
        class_name = agent_class.__name__
        if class_name not in self._agent_specs and class_name != "DummyAgent": # Allow DummyAgent without spec for now for testing purposes. Real agents will need specs.
             logger.warning(f"Attempted to register agent class {class_name} without a corresponding AgentSpec.")
        self._agents[class_name] = agent_class
        logger.info(f"Registered agent class: {class_name}")

    def get_agent_class(self, name: str) -> Optional[Type[Agent]]:
        """Retrieves an agent class by name.
        Looks up by agent_spec.name which might be different from class name,
        so we need a mapping or convention. For now, assuming agent_spec.name == class_name.
        """
        # A more robust solution might map agent_spec.name to a specific class path
        # For now, let's assume agent_spec.name is the class name (e.g., "DummyAgent" -> DummyAgent class)
        return self._agents.get(name)

    def get_agent_spec(self, name: str) -> Optional[AgentSpec]:
        """Retrieves an agent specification by name."""
        return self._agent_specs.get(name)

    def list_agent_specs(self) -> List[AgentSpec]:
        """Returns a list of all registered agent specifications."""
        return list(self._agent_specs.values())

agent_registry = AgentRegistry()
