# src/workflow/planner.py
"""Generates and validates workflow execution plans."""
from typing import List
from src.models import TaskSpec
from src.task_dependencies import topological_sort, detect_cycles

class WorkflowPlanner:
    def __init__(self):
        pass

    def generate_plan(self, tasks: List[TaskSpec]) -> List[TaskSpec]:
        """Generates an execution plan (topologically sorted tasks)."""
        if detect_cycles(tasks):
            raise ValueError("Workflow contains circular dependencies.")
        return topological_sort(tasks)

    def validate_plan(self, plan: List[TaskSpec]) -> bool:
        """Validates an execution plan."""
        # Placeholder for more complex validation logic
        return not detect_cycles(plan)
