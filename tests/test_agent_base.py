# tests/test_agent_base.py
import pytest
from abc import ABC, abstractmethod
from src.agents.base import Agent
from src.models import TaskSpec, AgentResponse
import uuid

def test_abstract_agent_cannot_be_instantiated():
    """Test that the abstract Agent class cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Agent(name="AbstractAgent")

def test_concrete_agent_implementation():
    """Test a concrete implementation of the Agent class."""
    class ConcreteAgent(Agent):
        def run(self, task: TaskSpec) -> AgentResponse:
            return AgentResponse(status="success", output={"task_id": task.id, "agent": self.name})

    agent = ConcreteAgent(name="MyConcreteAgent")
    assert agent.name == "MyConcreteAgent"

    task = TaskSpec(id=str(uuid.uuid4()), name="TestTask", description="Desc", agent_name="MyConcreteAgent")
    response = agent.run(task)
    assert isinstance(response, AgentResponse)
    assert response.status == "success"
    assert response.output["task_id"] == task.id
    assert response.output["agent"] == agent.name

def test_concrete_agent_missing_run_implementation():
    """Test that a concrete agent must implement the run method."""
    class InvalidAgent(Agent):
        # Missing run method
        pass

    with pytest.raises(TypeError):
        InvalidAgent(name="InvalidAgent")
