# tests/test_workflow_loader.py
import pytest
import os
import yaml
import json
from unittest.mock import patch
from src.workflow_loader import WorkflowLoader
from src.models import TaskSpec
from src.paths import get_root_dir

# Mock get_root_dir to use a temporary directory for tests
@pytest.fixture(autouse=True)
def mock_get_root_dir(tmp_path):
    with patch('src.paths.get_root_dir', return_value=str(tmp_path)):
        yield

@pytest.fixture
def create_test_workflow_files(tmp_path):
    """Fixture to create dummy workflow files in a temporary directory."""
    workflows_dir = os.path.join(str(tmp_path), "workflows")
    os.makedirs(workflows_dir, exist_ok=True)
    
    # Create a YAML workflow file
    yaml_content = {
        "name": "TestWorkflowYaml",
        "description": "A workflow from YAML",
        "tasks": [
            {"id": "task1", "name": "Task One", "description": "Desc 1", "agent_name": "AgentA", "dependencies": []},
            {"id": "task2", "name": "Task Two", "description": "Desc 2", "agent_name": "AgentB", "dependencies": ["task1"]}
        ]
    }
    with open(os.path.join(workflows_dir, "test_workflow.yaml"), "w") as f:
        yaml.dump(yaml_content, f)

    # Create a JSON workflow file
    json_content = {
        "name": "TestWorkflowJson",
        "description": "A workflow from JSON",
        "tasks": [
            {"id": "task_x", "name": "Task X", "description": "Desc X", "agent_name": "AgentX", "dependencies": []}
        ]
    }
    with open(os.path.join(workflows_dir, "test_workflow.json"), "w") as f:
        json.dump(json_content, f)
    
    # Create a file with unsupported type
    with open(os.path.join(workflows_dir, "unsupported.txt"), "w") as f:
        f.write("Some text")

    # Create an invalid workflow file (missing tasks)
    invalid_yaml_content = {
        "name": "InvalidWorkflow",
        "description": "Missing tasks key"
    }
    with open(os.path.join(workflows_dir, "invalid_workflow.yaml"), "w") as f:
        yaml.dump(invalid_yaml_content, f)

    return workflows_dir

def test_load_workflow_from_yaml(create_test_workflow_files):
    """Test loading a workflow from a YAML file."""
    loader = WorkflowLoader()
    tasks = loader.load_workflow_from_file("workflows/test_workflow.yaml")
    assert len(tasks) == 2
    assert isinstance(tasks[0], TaskSpec)
    assert tasks[0].id == "task1"
    assert tasks[1].dependencies == ["task1"]

def test_load_workflow_from_json(create_test_workflow_files):
    """Test loading a workflow from a JSON file."""
    loader = WorkflowLoader()
    tasks = loader.load_workflow_from_file("workflows/test_workflow.json")
    assert len(tasks) == 1
    assert tasks[0].id == "task_x"

def test_load_workflow_file_not_found():
    """Test loading a non-existent workflow file."""
    loader = WorkflowLoader()
    with pytest.raises(FileNotFoundError, match="Workflow file not found or unreadable"):
        loader.load_workflow_from_file("workflows/non_existent.yaml")

def test_load_workflow_unsupported_file_type(create_test_workflow_files):
    """Test loading a workflow from an unsupported file type."""
    loader = WorkflowLoader()
    with pytest.raises(ValueError, match="Unsupported workflow file type"):
        loader.load_workflow_from_file("workflows/unsupported.txt")

def test_load_workflow_invalid_yaml_format(tmp_path):
    """Test loading a workflow with invalid YAML syntax."""
    invalid_file_path = os.path.join(str(tmp_path), "workflows", "bad_syntax.yaml")
    os.makedirs(os.path.dirname(invalid_file_path), exist_ok=True)
    with open(invalid_file_path, "w") as f:
        f.write("tasks: -\n  id: task1") # Malformed YAML
    
    loader = WorkflowLoader()
    with pytest.raises(ValueError, match="Error parsing workflow file"):
        loader.load_workflow_from_file("workflows/bad_syntax.yaml")

def test_load_workflow_missing_tasks_key(create_test_workflow_files):
    """Test loading a workflow definition missing the 'tasks' key."""
    loader = WorkflowLoader()
    with pytest.raises(ValueError, match="Workflow 'tasks' key must be a list."):
        loader.load_workflow_from_file("workflows/invalid_workflow.yaml")

def test_load_workflow_tasks_not_list(tmp_path):
    """Test loading a workflow where 'tasks' is not a list."""
    invalid_file_path = os.path.join(str(tmp_path), "workflows", "tasks_not_list.yaml")
    os.makedirs(os.path.dirname(invalid_file_path), exist_ok=True)
    with open(invalid_file_path, "w") as f:
        yaml.dump({"name": "BadWorkflow", "tasks": "not_a_list"}, f)
    
    loader = WorkflowLoader()
    with pytest.raises(ValueError, match="Workflow 'tasks' key must be a list."):
        loader.load_workflow_from_file("workflows/tasks_not_list.yaml")

def test_load_workflow_invalid_task_spec_data(tmp_path):
    """Test loading a workflow with malformed task data."""
    invalid_file_path = os.path.join(str(tmp_path), "workflows", "bad_task_data.yaml")
    os.makedirs(os.path.dirname(invalid_file_path), exist_ok=True)
    with open(invalid_file_path, "w") as f:
        yaml.dump({
            "name": "BadWorkflow",
            "tasks": [
                {"id": "task1", "name": "Task One"} # Missing agent_name, description
            ]
        }, f)
    
    loader = WorkflowLoader()
    with pytest.raises(ValueError): # Pydantic ValidationError will be wrapped in ValueError
        loader.load_workflow_from_file("workflows/bad_task_data.yaml")
