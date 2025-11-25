# src/task_dependencies.py
"""Manages task dependencies, including topological sorting and cycle detection."""
from typing import List, Dict, Set, Tuple
from src.models import TaskSpec
import logging

logger = logging.getLogger(__name__)

def topological_sort(tasks: List[TaskSpec]) -> List[TaskSpec]:
    """
    Performs a topological sort on a list of tasks.
    Raises ValueError if a cycle is detected.
    """
    adj: Dict[str, List[str]] = {task.id: [] for task in tasks}
    in_degree: Dict[str, int] = {task.id: 0 for task in tasks}
    task_map: Dict[str, TaskSpec] = {task.id: task for task in tasks}

    for task in tasks:
        for dep_id in task.dependencies:
            if dep_id not in task_map:
                logger.warning(f"Dependency '{dep_id}' for task '{task.id}' not found in provided tasks. Skipping.")
                continue
            adj[dep_id].append(task.id)
            in_degree[task.id] += 1
    
    # Kahn's algorithm
    queue: List[str] = [task_id for task_id, degree in in_degree.items() if degree == 0]
    sorted_tasks_ids: List[str] = []

    while queue:
        u = queue.pop(0)
        sorted_tasks_ids.append(u)

        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    if len(sorted_tasks_ids) != len(tasks):
        raise ValueError("Circular dependency detected in tasks.")

    return [task_map[task_id] for task_id in sorted_tasks_ids]


def detect_cycles(tasks: List[TaskSpec]) -> bool:
    """
    Detects cycles in task dependencies using DFS.
    Returns True if a cycle is found, False otherwise.
    """
    adj: Dict[str, List[str]] = {task.id: [] for task in tasks}
    task_map: Dict[str, TaskSpec] = {task.id: task for task in tasks}

    for task in tasks:
        for dep_id in task.dependencies:
            if dep_id not in task_map:
                continue # Ignore dependencies not in the current set of tasks
            adj[task.id].append(dep_id) # Represent dependencies as edges from task to its dependency
    
    visited: Set[str] = set()
    recursion_stack: Set[str] = set()

    def dfs(u: str) -> bool:
        visited.add(u)
        recursion_stack.add(u)

        for v in adj[u]:
            if v not in visited:
                if dfs(v):
                    return True
            elif v in recursion_stack:
                return True
        
        recursion_stack.remove(u)
        return False
    
    for task_id in adj:
        if task_id not in visited:
            if dfs(task_id):
                return True
    
    return False
