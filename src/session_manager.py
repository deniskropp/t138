# src/session_manager.py
"""Manages individual session runs, persisting logs and artifacts."""
import uuid
import datetime
from typing import List
from src.models import Session, Artifact
from src.workflow.state import workflow_state_machine, WorkflowState
from src.artifacts import artifact_manager
import logging

class SessionManager:
    def __init__(self):
        self._current_session: Session = None # type: ignore
        self.logger = logging.getLogger(__name__)

    def start_session(self) -> Session:
        """Starts a new session."""
        session_id = str(uuid.uuid4())
        self._current_session = Session(
            id=session_id,
            start_time=datetime.datetime.now().isoformat(),
            status=WorkflowState.INIT.value,
            logs=[],
            artifacts=[]
        )
        workflow_state_machine.set_session(self._current_session)
        self.logger.info(f"Session {session_id} started.")
        return self._current_session

    def end_session(self, status: WorkflowState = WorkflowState.COMPLETED):
        """Ends the current session."""
        if self._current_session:
            self._current_session.end_time = datetime.datetime.now().isoformat()
            workflow_state_machine.transition_to(status)
            self.logger.info(f"Session {self._current_session.id} ended with status: {status.value}")
            # Persist session details (e.g., to DB or file)
            self._current_session = None

    def add_log_entry(self, entry: str):
        """Adds a log entry to the current session."""
        if self._current_session:
            self._current_session.logs.append(entry)

    def add_artifact(self, artifact: Artifact):
        """Adds an artifact to the current session and stores it."""
        if self._current_session:
            self._current_session.artifacts.append(artifact)
            artifact_manager.store_artifact(artifact, self._current_session.id)

    def get_current_session(self) -> Session:
        """Returns the current session object."""
        return self._current_session

session_manager = SessionManager()
