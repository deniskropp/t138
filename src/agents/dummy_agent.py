# src/agents/dummy_agent.py
"""A simple dummy agent for testing purposes."""
from src.agents.base import Agent
from src.models import TaskSpec, AgentResponse, Artifact
import logging
import random

logger = logging.getLogger(__name__)

class DummyAgent(Agent):
    def __init__(self, name: str = "DummyAgent"):
        super().__init__(name)
        logger.info(f"{self.name} initialized.")

    def run(self, task: TaskSpec) -> AgentResponse:
        logger.info(f"{self.name} received task: {task.name} (ID: {task.id})")
        logger.info(f"Input data: {task.input_data}")

        # Simulate some work
        if "fail_task" in task.input_data and task.input_data["fail_task"]:
            logger.error(f"{self.name} simulating failure for task {task.name}")
            return AgentResponse(
                status="failed",
                output={"error_message": f"Task {task.name} intentionally failed."},
                artifacts=[]
            )

        output_data = {
            "processed_by": self.name,
            "task_id": task.id,
            "random_number": random.randint(1, 100)
        }
        
        # Simulate creating an artifact
        artifact_content = f"Log for task {task.id}: {self.name} processed data."
        artifact = Artifact(name=f"task_{task.id}_log.txt", type="text/plain", data=artifact_content)

        logger.info(f"{self.name} completed task: {task.name}")
        return AgentResponse(
            status="completed",
            output=output_data,
            artifacts=[artifact]
        )
