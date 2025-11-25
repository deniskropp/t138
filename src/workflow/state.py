# src/workflow/state.py
"""Manages the state transitions of workflows."""
from enum import Enum
from src.models import Session

class WorkflowState(str, Enum):
    INIT = "INIT"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class WorkflowStateMachine:
    def __init__(self, initial_state: WorkflowState = WorkflowState.INIT):
        self._state = initial_state
        self._session: Session = None # type: ignore

    def set_session(self, session: Session):
        self._session = session

    def transition_to(self, new_state: WorkflowState):
        """Transitions the workflow to a new state."""
        self._state = new_state
        if self._session:
            self._session.status = new_state.value
        # Add state transition logic here
        pass

    def get_state(self) -> WorkflowState:
        """Returns the current state of the workflow."""
        return self._state

workflow_state_machine = WorkflowStateMachine()
