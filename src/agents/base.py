# src/agents/base.py
"""Defines the abstract base class for all agents."""
from abc import ABC, abstractmethod
from src.models import TaskSpec, AgentResponse

class Agent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, task: TaskSpec) -> AgentResponse:
        """Executes a given task and returns an AgentResponse."""
        pass
