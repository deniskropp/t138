# tests/test_agent_registry.py
import pytest
import os
from unittest.mock import patch, MagicMock
from src.agents.registry import AgentRegistry, agent_registry
from src.models import AgentSpec
from src.agents.base import Agent
import yaml
import json
import logging

# Mock get_root_dir to use a temporary directory for tests
@pytest.fixture(autouse=True)
def mock_get_root_dir(tmp_path):
    with patch('src.paths.get_root_dir', return_value=str(tmp_path)):
        yield

@pytest.fixture
def clean_agent_registry():
    """Fixture to ensure a clean agent_registry for each test."""
    original_specs = agent_registry._agent_specs.copy()
    original_agents = agent_registry._agents.copy()
    agent_registry._agent_specs.clear()
    agent_registry._agents.clear()
    yield
    agent_registry._agent_specs = original_specs
    agent_registry._agents = original_agents

@pytest.fixture
def create_test_agent_specs_in_registry(tmp_path):
    """Fixture to create dummy agent spec files and ensure they are loaded by registry."""
    spec_dir = os.path.join(str(tmp_path), "agents", "specs")
    os.makedirs(spec_dir, exist_ok=True)
    
    # Create a YAML spec file
    yaml_content = {
        "name": "TestAgent1",
        "role": "YamlProcessor",
        "description": "Agent 1."
    }
    with open(os.path.join(spec_dir, "test_agent1.yaml"), "w") as f:
        yaml.dump(yaml_content, f)

    # Create a JSON spec file
    json_content = {
        "name": "TestAgent2",
        "role": "JsonProcessor",
        "description": "Agent 2."
    }
    with open(os.path.join(spec_dir, "test_agent2.json"), "w") as f:
        json.dump(json_content, f)
    
    # Reload the registry to pick up new specs
    agent_registry._load_initial_agent_specs()
    
    # Define dummy agent classes for registration
    class ConcreteAgent1(Agent):
        def run(self, task):
            return MagicMock(spec=AgentResponse, status="success")

    class ConcreteAgent2(Agent):
        def run(self, task):
            return MagicMock(spec=AgentResponse, status="success")

    # Register agent classes
    agent_registry.register_agent_class(ConcreteAgent1)
    agent_registry.register_agent_class(ConcreteAgent2)

def test_agent_registry_loads_specs_on_init(clean_agent_registry, create_test_agent_specs_in_registry):
    """Test that agent specifications are loaded automatically on registry initialization."""
    assert agent_registry.get_agent_spec("TestAgent1") is not None
    assert agent_registry.get_agent_spec("TestAgent2") is not None
    assert len(agent_registry.list_agent_specs()) == 2

def test_agent_registry_get_agent_spec(clean_agent_registry, create_test_agent_specs_in_registry):
    """Test retrieving an agent specification by name."""
    spec = agent_registry.get_agent_spec("TestAgent1")
    assert spec.name == "TestAgent1"
    assert spec.role == "YamlProcessor"
    
    assert agent_registry.get_agent_spec("NonExistentAgent") is None

def test_agent_registry_register_and_get_agent_class(clean_agent_registry, create_test_agent_specs_in_registry):
    """Test registering and retrieving agent classes."""
    class MyCustomAgent(Agent):
        def run(self, task):
            pass
    
    spec = AgentSpec(name="MyCustomAgent", role="Custom", description="A custom agent.")
    agent_registry._agent_specs["MyCustomAgent"] = spec # Manually add spec for this test
    agent_registry.register_agent_class(MyCustomAgent)

    retrieved_class = agent_registry.get_agent_class("MyCustomAgent")
    assert retrieved_class == MyCustomAgent

    assert agent_registry.get_agent_class("NonExistentAgent") is None

def test_agent_registry_list_agent_specs(clean_agent_registry, create_test_agent_specs_in_registry):
    """Test listing all registered agent specifications."""
    specs = agent_registry.list_agent_specs()
    names = {s.name for s in specs}
    assert "TestAgent1" in names
    assert "TestAgent2" in names
    assert len(names) == 2

def test_agent_registry_warns_on_class_without_spec(clean_agent_registry, caplog):
    """Test that a warning is logged if an agent class is registered without a corresponding spec."""
    class NoSpecAgent(Agent):
        def run(self, task):
            pass

    with caplog.at_level(logging.WARNING):
        agent_registry.register_agent_class(NoSpecAgent)
        assert "Attempted to register agent class NoSpecAgent without a corresponding AgentSpec." in caplog.text
