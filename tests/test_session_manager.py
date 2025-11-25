# tests/test_session_manager.py
import pytest
import uuid
import datetime
from unittest.mock import patch, MagicMock
from src.session_manager import SessionManager
from src.models import Session, Artifact
from src.workflow.state import WorkflowState
from src.artifacts import artifact_manager
from src.workflow.state import workflow_state_machine

@pytest.fixture
def clean_session_manager():
    """Provides a fresh SessionManager instance for each test."""
    manager = SessionManager()
    # Reset workflow_state_machine and artifact_manager for clean state
    workflow_state_machine._state = WorkflowState.INIT
    workflow_state_machine._session = None
    # No need to clear artifact_manager's internal state as it's mocked in tests
    return manager

def test_start_session(clean_session_manager):
    """Test starting a new session."""
    session = clean_session_manager.start_session()
    assert isinstance(session, Session)
    assert session.id is not None
    assert session.status == WorkflowState.INIT.value
    assert session.start_time is not None
    assert clean_session_manager.get_current_session() == session
    assert workflow_state_machine.get_state() == WorkflowState.INIT
    assert workflow_state_machine._session == session # Ensure session is set in state machine

def test_end_session(clean_session_manager):
    """Test ending a session."""
    session = clean_session_manager.start_session()
    clean_session_manager.end_session()
    
    assert session.end_time is not None
    assert session.status == WorkflowState.COMPLETED.value
    assert workflow_state_machine.get_state() == WorkflowState.COMPLETED
    assert clean_session_manager.get_current_session() is None

def test_end_session_with_failed_status(clean_session_manager):
    """Test ending a session with a specific status like FAILED."""
    session = clean_session_manager.start_session()
    clean_session_manager.end_session(status=WorkflowState.FAILED)
    
    assert session.end_time is not None
    assert session.status == WorkflowState.FAILED.value
    assert workflow_state_machine.get_state() == WorkflowState.FAILED

def test_add_log_entry(clean_session_manager):
    """Test adding log entries to a session."""
    session = clean_session_manager.start_session()
    clean_session_manager.add_log_entry("Log entry 1")
    clean_session_manager.add_log_entry("Log entry 2")
    assert session.logs == ["Log entry 1", "Log entry 2"]

@patch('src.artifacts.artifact_manager.store_artifact')
def test_add_artifact(mock_store_artifact, clean_session_manager):
    """Test adding an artifact to a session and ensuring it's stored."""
    session = clean_session_manager.start_session()
    artifact = Artifact(name="test.txt", type="text", data="hello")
    clean_session_manager.add_artifact(artifact)
    
    assert len(session.artifacts) == 1
    assert session.artifacts[0] == artifact
    mock_store_artifact.assert_called_once_with(artifact, session.id)

def test_get_current_session(clean_session_manager):
    """Test retrieving the current session."""
    assert clean_session_manager.get_current_session() is None
    session = clean_session_manager.start_session()
    assert clean_session_manager.get_current_session() == session
