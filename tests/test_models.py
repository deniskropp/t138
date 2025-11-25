# tests/test_models.py
import pytest
from pydantic import ValidationError
from src.models import AgentSpec, TaskSpec, Artifact, Session, ExecutionContext, AgentResponse
import uuid
import datetime

def test_agent_spec_model():
    """Test AgentSpec model validation."""
    spec = AgentSpec(name="TestAgent", role="TestRole", description="A test agent.")
    assert spec.name == "TestAgent"
    assert spec.role == "TestRole"
    assert spec.description == "A test agent."

    with pytest.raises(ValidationError):
        AgentSpec(name="TestAgent", role="TestRole") # Missing description

def test_task_spec_model():
    """Test TaskSpec model validation."""
    task = TaskSpec(id=str(uuid.uuid4()), name="TestTask", description="A test task.", agent_name="TestAgent")
    assert task.name == "TestTask"
    assert task.input_data == {}
    assert task.dependencies == []

def test_artifact_model():
    """Test Artifact model validation."""
    artifact = Artifact(name="report.pdf", type="document", data={"url": "http://example.com/report.pdf"})
    assert artifact.name == "report.pdf"
    assert artifact.type == "document"
    assert artifact.data == {"url": "http://example.com/report.pdf"}

def test_session_model():
    """Test Session model validation."""
    session_id = str(uuid.uuid4())
    start_time = datetime.datetime.now().isoformat()
    session = Session(id=session_id, start_time=start_time, status="RUNNING")
    assert session.id == session_id
    assert session.status == "RUNNING"
    assert session.end_time is None
    assert session.logs == []
    assert session.artifacts == []

def test_execution_context_model():
    """Test ExecutionContext model validation."""
    context = ExecutionContext(session_id=str(uuid.uuid4()))
    assert context.env_vars == {}
    assert context.runtime_flags == {}
    assert context.current_task_id is None

def test_agent_response_model():
    """Test AgentResponse model validation."""
    response = AgentResponse(status="success", output={"result": "done"})
    assert response.status == "success"
    assert response.output == {"result": "done"}
    assert response.artifacts == []

    artifact = Artifact(name="log.txt", type="text", data="log content")
    response_with_artifact = AgentResponse(status="success", artifacts=[artifact])
    assert len(response_with_artifact.artifacts) == 1
    assert response_with_artifact.artifacts[0].name == "log.txt"
