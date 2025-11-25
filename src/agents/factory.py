# src/agents/factory.py
"""Factory for creating concrete agent instances from specifications."""
from src.agents.base import Agent
from src.agents.registry import agent_registry
from src.models import AgentSpec # Keep for type hinting if needed

class AgentFactory:
    def create_agent(self, agent_name: str) -> Agent:
        """
        Creates an agent instance from an agent's name.
        Looks up the AgentSpec in the registry and instantiates the
        corresponding Agent class.
        """
        agent_spec = agent_registry.get_agent_spec(agent_name)
        if not agent_spec:
            raise ValueError(f"Agent specification for '{agent_name}' not found in registry.")
        
        # This is a simplification. In a real system, you'd dynamically import
        # the agent class based on the spec or have a more sophisticated mapping.
        # For now, we'll assume the agent_class is registered with its name.
        agent_class = agent_registry.get_agent_class(agent_name)
        if agent_class:
            return agent_class(agent_name)
        raise ValueError(f"Agent class for '{agent_name}' not found in registry.")
