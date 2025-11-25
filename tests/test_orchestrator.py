import pytest
from unittest.mock import MagicMock, patch, call
import uuid
from src.orchestrator import Orchestrator
from src.agents.factory import AgentFactory
from src.models import TaskSpec, AgentResponse, Artifact
from src.task_manager import task_queue
from src.workflow.state import workflow_state_machine, WorkflowState
from src.session_manager import session_manager
from src.task_dependencies import topological_sort, detect_cycles

@pytest.fixture(autouse=True)
def mock_dependencies():
    """Mock external dependencies for Orchestrator tests."""
    with patch('src.task_manager.task_queue.get_next_task') as mock_get_next_task, \
         patch('src.task_manager.task_queue.update_task_status') as mock_update_task_status, \
         patch('src.task_manager.task_queue.add_task') as mock_add_task, \
         patch('src.session_manager.session_manager.get_current_session') as mock_get_current_session, \
         patch('src.session_manager.session_manager.add_log_entry') as mock_add_log_entry, \
         patch('src.session_manager.session_manager.add_artifact') as mock_add_artifact, \
         patch('src.session_manager.session_manager.end_session') as mock_end_session, \
         patch('src.agents.factory.AgentFactory.create_agent') as mock_create_agent, \
         patch('src.workflow.state.workflow_state_machine.transition_to') as mock_transition_to, \
         patch('src.workflow.state.workflow_state_machine.get_state') as mock_get_state:
        
        # Default mock for get_current_session to return a valid session
        mock_session = MagicMock(spec=session_manager.get_current_session())
        mock_session.id = str(uuid.uuid4())
        mock_get_current_session.return_value = mock_session

        # Default mock for get_state
        mock_get_state.side_effect = [
            WorkflowState.RUNNING, # Initial transition
            WorkflowState.RUNNING, # After first task
            WorkflowState.RUNNING, # After second task
            WorkflowState.RUNNING, # Final check before completion
            WorkflowState.COMPLETED # End state
        ]
        
        yield mock_get_next_task, mock_update_task_status, mock_add_task, \
              mock_get_current_session, mock_add_log_entry, mock_add_artifact, \
              mock_end_session, mock_create_agent, mock_transition_to, mock_get_state

@pytest.fixture
def agent_factory_instance():
    """Provides a mock AgentFactory instance."""
    return AgentFactory()

def create_task_spec(id: str, dependencies: list = None) -> TaskSpec:
    """Helper to create TaskSpec objects."""
    return TaskSpec(id=id, name=id, description=f"Task {id}", agent_name=f"Agent{id[-1]}", dependencies=dependencies if dependencies is not None else [])


def test_orchestrator_runs_workflow_successfully(agent_factory_instance, mock_dependencies):
    """Test that the orchestrator runs a workflow with multiple tasks successfully."""
    mock_get_next_task, mock_update_task_status, mock_add_task, \
        mock_get_current_session, mock_add_log_entry, mock_add_artifact, \
        mock_end_session, mock_create_agent, mock_transition_to, mock_get_state = mock_dependencies

    # Setup tasks for the orchestrator
    task1 = create_task_spec("task1")
    task2 = create_task_spec("task2", dependencies=["task1"])
    initial_tasks = [task2, task1] # Not yet sorted

    # Mock get_next_task to return tasks in sorted order
    mock_get_next_task.side_effect = [task1, task2, None] 

    mock_agent1 = MagicMock()
    mock_agent1.run.return_value = AgentResponse(status="completed", output={"result": "task1_done"})
    mock_agent2 = MagicMock()
    mock_agent2.run.return_value = AgentResponse(status="completed", output={"result": "task2_done"})
    mock_create_agent.side_effect = [mock_agent1, mock_agent2]

    orchestrator = Orchestrator(agent_factory_instance)
    orchestrator.run_workflow(initial_tasks)

    # Verify task queue was populated in correct order
    mock_add_task.assert_has_calls([call(task1), call(task2)], any_order=False)

    mock_transition_to.assert_has_calls([
        call(WorkflowState.RUNNING)
    ])
    assert mock_get_next_task.call_count == 3
    assert mock_create_agent.call_count == 2
    assert mock_agent1.run.call_count == 1
    assert mock_agent2.run.call_count == 1
    mock_update_task_status.assert_has_calls([
        call("task1", "completed"),
        call("task2", "completed")
    ])
    mock_end_session.assert_called_once_with(status=WorkflowState.COMPLETED)
    assert mock_add_log_entry.call_count >= 2 # At least for dispatching tasks


def test_orchestrator_stops_on_agent_failure_status(agent_factory_instance, mock_dependencies):
    """Test that the orchestrator stops the workflow if an agent returns a 'failed' status."""
    mock_get_next_task, mock_update_task_status, mock_add_task, \
        mock_get_current_session, mock_add_log_entry, mock_add_artifact, \
        mock_end_session, mock_create_agent, mock_transition_to, mock_get_state = mock_dependencies

    task1 = create_task_spec("task1")
    task2 = create_task_spec("task2", dependencies=["task1"])
    initial_tasks = [task1, task2]

    mock_get_next_task.side_effect = [task1, task2, None]

    mock_agent1 = MagicMock()
    mock_agent1.run.return_value = AgentResponse(status="failed", output={"error_message": "Agent failed"})
    mock_create_agent.return_value = mock_agent1 # Only agent1 will be created

    orchestrator = Orchestrator(agent_factory_instance)
    orchestrator.run_workflow(initial_tasks)

    mock_transition_to.assert_has_calls([
        call(WorkflowState.RUNNING),
        call(WorkflowState.FAILED)
    ])
    assert mock_add_task.call_count == 2 # Tasks added to queue
    assert mock_get_next_task.call_count == 2 # Called for task1, then for task2, but agent1 failed
    mock_update_task_status.assert_called_once_with("task1", "failed")
    mock_end_session.assert_called_once_with(status=WorkflowState.FAILED)
    # The factory should be called once to create Agent for task1,
    # but not for task2 as the workflow stops.
    mock_create_agent.assert_called_once_with("Agent1")


def test_orchestrator_stops_on_exception(agent_factory_instance, mock_dependencies):
    """Test that the orchestrator stops the workflow if an exception occurs during task execution."""
    mock_get_next_task, mock_update_task_status, mock_add_task, \
        mock_get_current_session, mock_add_log_entry, mock_add_artifact, \
        mock_end_session, mock_create_agent, mock_transition_to, mock_get_state = mock_dependencies

    task1 = create_task_spec("task1")
    task2 = create_task_spec("task2", dependencies=["task1"])
    initial_tasks = [task1, task2]

    mock_get_next_task.side_effect = [task1, task2, None]

    mock_agent1 = MagicMock()
    mock_agent1.run.side_effect = Exception("Simulated agent runtime error")
    mock_create_agent.return_value = mock_agent1

    orchestrator = Orchestrator(agent_factory_instance)
    orchestrator.run_workflow(initial_tasks)

    mock_transition_to.assert_has_calls([
        call(WorkflowState.RUNNING),
        call(WorkflowState.FAILED)
    ])
    assert mock_add_task.call_count == 2
    assert mock_get_next_task.call_count == 2
    mock_update_task_status.assert_called_once_with("task1", "failed")
    mock_end_session.assert_called_once_with(status=WorkflowState.FAILED)


def test_orchestrator_adds_artifacts_to_session(agent_factory_instance, mock_dependencies):
    """Test that artifacts returned by agents are added to the session manager."""
    mock_get_next_task, mock_update_task_status, mock_add_task, \
        mock_get_current_session, mock_add_log_entry, mock_add_artifact, \
        mock_end_session, mock_create_agent, mock_transition_to, mock_get_state = mock_dependencies

    task1 = create_task_spec("task1")
    initial_tasks = [task1]

    mock_get_next_task.side_effect = [task1, None]

    artifact = Artifact(name="report.txt", type="text", data="Report content")
    mock_agent1 = MagicMock()
    mock_agent1.run.return_value = AgentResponse(status="completed", artifacts=[artifact])
    mock_create_agent.return_value = mock_agent1

    orchestrator = Orchestrator(agent_factory_instance)
    orchestrator.run_workflow(initial_tasks)

    mock_add_artifact.assert_called_once_with(artifact)

def test_orchestrator_detects_circular_dependencies(agent_factory_instance, mock_dependencies):
    """Test that the orchestrator detects and handles circular dependencies."""
    mock_get_next_task, mock_update_task_status, mock_add_task, \
        mock_get_current_session, mock_add_log_entry, mock_add_artifact, \
        mock_end_session, mock_create_agent, mock_transition_to, mock_get_state = mock_dependencies

    task1 = create_task_spec("task1", dependencies=["task2"])
    task2 = create_task_spec("task2", dependencies=["task1"])
    initial_tasks = [task1, task2]

    orchestrator = Orchestrator(agent_factory_instance)
    orchestrator.run_workflow(initial_tasks)

    mock_transition_to.assert_has_calls([
        call(WorkflowState.RUNNING),
        call(WorkflowState.FAILED)
    ])
    # The workflow should fail before adding tasks to the queue or creating agents
    mock_add_task.assert_not_called()
    mock_create_agent.assert_not_called()
    mock_end_session.assert_called_once_with(status=WorkflowState.FAILED)
    # Check that an error log related to circular dependency is made
    mock_add_log_entry.assert_any_call(f"Workflow failed due to dependency issue: Circular dependency detected in the initial task list.")
