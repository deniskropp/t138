# tests/test_bootstrap.py
import pytest
from unittest.mock import patch, MagicMock, call
import os
from src.bootstrap import bootstrap_system
from src.config import settings
from src.paths import get_root_dir, ensure_dir
from src.logger import setup_logging
from src.llms.client import llm_client
from src.agents.registry import agent_registry
from src.session_manager import session_manager
from src.workflow.state import workflow_state_machine

@pytest.fixture(autouse=True)
def mock_dependencies(monkeypatch, tmp_path):
    """Mock external dependencies for bootstrap_system."""
    # Mock paths
    monkeypatch.setattr('src.paths.get_root_dir', lambda: str(tmp_path))
    monkeypatch.setattr('src.paths.ensure_dir', MagicMock())

    # Mock logging
    monkeypatch.setattr('src.logger.setup_logging', MagicMock())
    monkeypatch.setattr('logging.info', MagicMock())
    monkeypatch.setattr('logging.getLogger', MagicMock(return_value=MagicMock()))

    # Mock LLM client
    monkeypatch.setattr('src.llms.client.llm_client._initialize_providers', MagicMock())

    # Mock agent registry
    monkeypatch.setattr('src.agents.registry.agent_registry._load_initial_agent_specs', MagicMock())

    # Mock session manager
    monkeypatch.setattr('src.session_manager.session_manager.start_session', MagicMock(return_value=MagicMock()))

    # Mock settings to avoid actual file loading
    monkeypatch.setattr(settings, "APP_NAME", "TestApp")
    monkeypatch.setattr(settings, "LOG_LEVEL", "INFO")
    monkeypatch.setattr(settings, "PROMPTS_DIR", "prompts")
    monkeypatch.setattr(settings, "ARTIFACTS_DIR", "artifacts")
    monkeypatch.setattr(settings, "ACTIVE_LLM_PROVIDERS", "") # Ensure no actual LLM init tries to happen

def test_bootstrap_system_calls_dependencies_in_order(mock_dependencies):
    """Test that bootstrap_system calls its dependencies in the correct order."""
    bootstrap_system()

    mock_ensure_dir = src.paths.ensure_dir
    mock_setup_logging = src.logger.setup_logging
    mock_llm_initialize_providers = src.llms.client.llm_client._initialize_providers
    mock_agent_load_specs = src.agents.registry.agent_registry._load_initial_agent_specs
    mock_session_start = src.session_manager.session_manager.start_session

    # Verify calls
    mock_ensure_dir.assert_has_calls([
        call(os.path.join(get_root_dir())),
        call(os.path.join(get_root_dir(), "logs")),
        call(os.path.join(get_root_dir(), "artifacts")),
        call(os.path.join(get_root_dir(), "prompts")),
        call(os.path.join(get_root_dir(), "agents/specs"))
    ])
    
    # Ensure sequential calls in the correct order (conceptually, not strict mock order for all)
    # This is tricky with multiple mocks, but we can check if they were called
    # and use logging.info calls to assert sequence.
    assert mock_setup_logging.called
    assert mock_llm_initialize_providers.called
    assert mock_agent_load_specs.called
    assert mock_session_start.called

    # More robust sequence check using logging calls
    log_calls = [c.args[0] for c in logging.info.call_args_list]
    assert "Starting system bootstrap..." in log_calls
    assert "Logging configured." in log_calls
    assert "LLM client initialized." in log_calls
    assert "Agent registry loaded with specifications." in log_calls
    assert "Session manager initialized." in log_calls
    assert "System bootstrap complete." in log_calls

    # Verify the relative order
    assert log_calls.index("Logging configured.") < log_calls.index("LLM client initialized.")
    assert log_calls.index("LLM client initialized.") < log_calls.index("Agent registry loaded with specifications.")
    assert log_calls.index("Agent registry loaded with specifications.") < log_calls.index("Session manager initialized.")
