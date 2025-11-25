# tests/test_agent_factory.py
import pytest
from unittest.mock import MagicMock
from src.agents.factory import AgentFactory
from src.agents.base import Agent
from src.agents.registry import agent_registry
from src.models import AgentSpec, AgentResponse

# Fixture to ensure a clean registry and some dummy agent specs/classes for testing
@pytest.fixture(autouse=True)
def setup_agent_registry():
    # Clear registry before test
    agent_registry._agent_specs.clear()
    agent_registry._agents.clear()

    # Create dummy AgentSpec
    spec1 = AgentSpec(name="TestAgent1", role="Role1", description="Desc1")
    spec2 = AgentSpec(name="TestAgent2", role="Role2", description="Desc2")
    
    agent_registry._agent_specs["TestAgent1"] = spec1
    agent_registry._agent_specs["TestAgent2"] = spec2

    # Create dummy Agent classes
    class MockAgent1(Agent):
        def run(self, task):
            return MagicMock(spec=AgentResponse, status="success", output={"agent": self.name})
    
    class MockAgent2(Agent):
        def run(self, task):
            return MagicMock(spec=AgentResponse, status="success", output={"agent": self.name})

    # Register classes
    agent_registry.register_agent_class(MockAgent1)
    agent_registry.register_agent_class(MockAgent2) # This class won't have a spec entry, will warn

    # Also register for existing specs
    agent_registry._agents["TestAgent1"] = MockAgent1
    agent_registry._agents["TestAgent2"] = MockAgent2 # This will map the registered class to the spec name

    yield

    # Clean up registry after test
    agent_registry._agent_specs.clear()
    agent_registry._agents.clear()

def test_agent_factory_creates_agent_successfully():
    """Test that the AgentFactory correctly creates an agent instance."""
    factory = AgentFactory()
    agent_instance = factory.create_agent("TestAgent1")
    assert isinstance(agent_instance, Agent)
    assert agent_instance.name == "TestAgent1"

def test_agent_factory_raises_error_for_unknown_agent_spec():
    """Test that an error is raised if the AgentSpec is not found."""
    factory = AgentFactory()
    with pytest.raises(ValueError, match="Agent specification for 'UnknownAgent' not found in registry."):
        factory.create_agent("UnknownAgent")

def test_agent_factory_raises_error_for_unknown_agent_class():
    """Test that an error is raised if the Agent class is not found for a spec."""
    # Temporarily remove a class from the registry
    del agent_registry._agents["TestAgent1"]
    
    factory = AgentFactory()
    with pytest.raises(ValueError, match="Agent class for 'TestAgent1' not found in registry."):
        factory.create_agent("TestAgent1")

def test_agent_factory_creates_multiple_agents():
    """Test creating different agent instances."""
    factory = AgentFactory()
    agent1 = factory.create_agent("TestAgent1")
    agent2 = factory.create_agent("TestAgent2")
    
    assert agent1.name == "TestAgent1"
    assert agent2.name == "TestAgent2"
    assert agent1 is not agent2 # Ensure separate instances
