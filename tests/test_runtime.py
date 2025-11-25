# tests/test_runtime.py
import pytest
from unittest.mock import MagicMock, patch
from src.runtime import SystemRuntime, system_runtime
from src.config import Settings
from src.agents.registry import AgentRegistry
from src.session_manager import SessionManager
import logging

@pytest.fixture
def mock_runtime_dependencies(monkeypatch):
    """Mock dependencies for SystemRuntime to prevent actual initialization side effects."""
    monkeypatch.setattr('src.config.settings', MagicMock(spec=Settings))
    monkeypatch.setattr('src.agents.registry.agent_registry', MagicMock(spec=AgentRegistry))
    monkeypatch.setattr('src.session_manager.session_manager', MagicMock(spec=SessionManager))
    monkeypatch.setattr('logging.getLogger', MagicMock(return_value=MagicMock()))

def test_system_runtime_initialization(mock_runtime_dependencies):
    """Test that SystemRuntime initializes its components correctly."""
    runtime = SystemRuntime()
    assert runtime.config is src.config.settings
    assert runtime.agent_registry is src.agents.registry.agent_registry
    assert runtime.session_manager is src.session_manager.session_manager
    assert isinstance(runtime.logger, MagicMock) # Mocked logger

def test_global_system_runtime_instance(mock_runtime_dependencies):
    """Test that system_runtime is a singleton instance."""
    first_instance = system_runtime
    second_instance = system_runtime # Accessing the imported global instance again
    assert first_instance is second_instance

    # Verify that re-instantiating the class creates a new object
    new_instance = SystemRuntime()
    assert new_instance is not first_instance
