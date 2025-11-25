# tests/test_context.py
import pytest
from src.context import ContextManager
from src.models import ExecutionContext
import uuid

@pytest.fixture
def clean_context_manager():
    """Provides a clean ContextManager instance for each test."""
    return ContextManager()

def test_initial_execution_context(clean_context_manager):
    """Test that the initial context is created with a default session ID."""
    context = clean_context_manager.get_context()
    assert isinstance(context, ExecutionContext)
    assert context.session_id == "default"
    assert context.env_vars == {}
    assert context.runtime_flags == {}
    assert context.current_task_id is None

def test_set_context(clean_context_manager):
    """Test setting a new execution context."""
    new_session_id = str(uuid.uuid4())
    new_context = ExecutionContext(
        session_id=new_session_id,
        env_vars={"ENV_VAR": "value"},
        runtime_flags={"FLAG_A": True},
        current_task_id="task-123"
    )
    clean_context_manager.set_context(new_context)
    retrieved_context = clean_context_manager.get_context()
    assert retrieved_context == new_context

def test_update_env_var(clean_context_manager):
    """Test updating an environment variable in the context."""
    clean_context_manager.update_env_var("MY_ENV", "my_value")
    assert clean_context_manager.get_context().env_vars["MY_ENV"] == "my_value"
    clean_context_manager.update_env_var("MY_ENV", "new_value")
    assert clean_context_manager.get_context().env_vars["MY_ENV"] == "new_value"

def test_update_runtime_flag(clean_context_manager):
    """Test updating a runtime flag in the context."""
    clean_context_manager.update_runtime_flag("DRY_RUN", True)
    assert clean_context_manager.get_context().runtime_flags["DRY_RUN"] is True
    clean_context_manager.update_runtime_flag("VERBOSE", 1)
    assert clean_context_manager.get_context().runtime_flags["VERBOSE"] == 1

def test_current_task_id_update():
    """Test updating the current task ID (indirectly through ExecutionContext)."""
    context_mgr = ContextManager()
    initial_context = context_mgr.get_context()
    
    # Simulate updating current_task_id directly on the context object
    # In a real scenario, an orchestrator would likely do this.
    initial_context.current_task_id = "task-456"
    
    retrieved_context = context_mgr.get_context()
    assert retrieved_context.current_task_id == "task-456"
