# tests/test_workflow_state.py
import pytest
from src.workflow.state import WorkflowState, WorkflowStateMachine
from src.models import Session
import uuid
import datetime

@pytest.fixture
def clean_state_machine():
    """Provides a fresh WorkflowStateMachine instance for each test."""
    return WorkflowStateMachine()

@pytest.fixture
def mock_session():
    """Provides a mock Session object."""
    return Session(
        id=str(uuid.uuid4()),
        start_time=datetime.datetime.now().isoformat(),
        status=WorkflowState.INIT.value
    )

def test_initial_state(clean_state_machine):
    """Test that the initial state is INIT."""
    assert clean_state_machine.get_state() == WorkflowState.INIT

def test_transition_to_state(clean_state_machine, mock_session):
    """Test state transitions update both the state machine and the session."""
    clean_state_machine.set_session(mock_session)
    assert clean_state_machine.get_state() == WorkflowState.INIT
    assert mock_session.status == WorkflowState.INIT.value

    clean_state_machine.transition_to(WorkflowState.RUNNING)
    assert clean_state_machine.get_state() == WorkflowState.RUNNING
    assert mock_session.status == WorkflowState.RUNNING.value

    clean_state_machine.transition_to(WorkflowState.COMPLETED)
    assert clean_state_machine.get_state() == WorkflowState.COMPLETED
    assert mock_session.status == WorkflowState.COMPLETED.value

def test_transition_to_failed_state(clean_state_machine, mock_session):
    """Test transitioning to the FAILED state."""
    clean_state_machine.set_session(mock_session)
    clean_state_machine.transition_to(WorkflowState.FAILED)
    assert clean_state_machine.get_state() == WorkflowState.FAILED
    assert mock_session.status == WorkflowState.FAILED.value

def test_set_session_updates_status_reference(clean_state_machine):
    """Test that setting a session correctly links its status."""
    session1 = Session(id="1", start_time="...", status="INIT")
    session2 = Session(id="2", start_time="...", status="RUNNING")

    clean_state_machine.set_session(session1)
    clean_state_machine.transition_to(WorkflowState.RUNNING)
    assert session1.status == WorkflowState.RUNNING.value

    clean_state_machine.set_session(session2)
    clean_state_machine.transition_to(WorkflowState.COMPLETED)
    assert session2.status == WorkflowState.COMPLETED.value
    assert session1.status == WorkflowState.RUNNING.value # Old session status remains as it was
