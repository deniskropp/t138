# tests/test_workflow_planner.py
import pytest
from unittest.mock import patch, MagicMock
from src.workflow.planner import WorkflowPlanner
from src.models import TaskSpec
from src.task_dependencies import topological_sort, detect_cycles

# Mock the dependency functions to control their behavior for testing the planner
@pytest.fixture(autouse=True)
def mock_dependency_functions(monkeypatch):
    """Mock topological_sort and detect_cycles."""
    monkeypatch.setattr('src.task_dependencies.topological_sort', MagicMock(side_effect=lambda x: x))
    monkeypatch.setattr('src.task_dependencies.detect_cycles', MagicMock(return_value=False))

@pytest.fixture
def clean_workflow_planner():
    """Provides a fresh WorkflowPlanner instance for each test."""
    return WorkflowPlanner()

def create_task_spec(id: str, dependencies: list = None) -> TaskSpec:
    """Helper to create TaskSpec objects."""
    return TaskSpec(id=id, name=id, description=f"Task {id}", agent_name=f"Agent{id[-1]}", dependencies=dependencies if dependencies is not None else [])


def test_generate_plan_no_cycles(clean_workflow_planner, mock_dependency_functions):
    """Test that generate_plan calls topological_sort when no cycles are detected."""
    tasks = [
        create_task_spec("A"),
        create_task_spec("B", dependencies=["A"])
    ]
    
    plan = clean_workflow_planner.generate_plan(tasks)
    
    mock_dependency_functions['detect_cycles'].assert_called_once_with(tasks)
    mock_dependency_functions['topological_sort'].assert_called_once_with(tasks)
    assert plan == tasks # Because topological_sort is mocked to return original list

def test_generate_plan_with_cycles_raises_error(clean_workflow_planner, mock_dependency_functions):
    """Test that generate_plan raises an error when cycles are detected."""
    tasks = [
        create_task_spec("A", dependencies=["B"]),
        create_task_spec("B", dependencies=["A"])
    ]
    
    mock_dependency_functions['detect_cycles'].return_value = True
    
    with pytest.raises(ValueError, match="Workflow contains circular dependencies."):
        clean_workflow_planner.generate_plan(tasks)
    
    mock_dependency_functions['detect_cycles'].assert_called_once_with(tasks)
    mock_dependency_functions['topological_sort'].assert_not_called() # Should not proceed to sort

def test_validate_plan_no_cycles(clean_workflow_planner, mock_dependency_functions):
    """Test that validate_plan returns True when no cycles are detected."""
    tasks = [
        create_task_spec("A"),
        create_task_spec("B", dependencies=["A"])
    ]
    
    is_valid = clean_workflow_planner.validate_plan(tasks)
    
    mock_dependency_functions['detect_cycles'].assert_called_once_with(tasks)
    assert is_valid is True

def test_validate_plan_with_cycles(clean_workflow_planner, mock_dependency_functions):
    """Test that validate_plan returns False when cycles are detected."""
    tasks = [
        create_task_spec("A", dependencies=["B"]),
        create_task_spec("B", dependencies=["A"])
    ]
    
    mock_dependency_functions['detect_cycles'].return_value = True
    
    is_valid = clean_workflow_planner.validate_plan(tasks)
    
    mock_dependency_functions['detect_cycles'].assert_called_once_with(tasks)
    assert is_valid is False
