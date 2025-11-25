# src/task_manager.py
"""Core module for managing tasks, queues, and status."""
from collections import deque
from typing import Deque, Dict, Optional
from src.models import TaskSpec

class TaskQueue:
    def __init__(self):
        self._queue: Deque[TaskSpec] = deque()
        self._status: Dict[str, str] = {} # task_id -> status

    def add_task(self, task: TaskSpec):
        """Adds a task to the queue."""
        self._queue.append(task)
        self._status[task.id] = "pending"

    def get_next_task(self) -> Optional[TaskSpec]:
        """Retrieves the next task from the queue."""
        if self._queue:
            task = self._queue.popleft()
            self._status[task.id] = "in_progress"
            return task
        return None

    def update_task_status(self, task_id: str, status: str):
        """Updates the status of a task."""
        if task_id in self._status:
            self._status[task_id] = status

    def get_task_status(self, task_id: str) -> Optional[str]:
        """Returns the status of a task."""
        return self._status.get(task_id)

task_queue = TaskQueue()
