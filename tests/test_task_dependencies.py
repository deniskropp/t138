# tests/test_task_dependencies.py
import pytest
from src.task_dependencies import topological_sort, detect_cycles
from src.models import TaskSpec
import uuid

def create_task(name: str, dependencies: list[str]) -> TaskSpec:
    """Helper to create TaskSpec objects."""
    return TaskSpec(id=name, name=name, description=f"Task {name}", agent_name="AgentX", dependencies=dependencies)

def test_topological_sort_no_dependencies():
    """Test topological sort with no dependencies."""
    tasks = [
        create_task("A", []),
        create_task("B", []),
        create_task("C", [])
    ]
    sorted_tasks = topological_sort(tasks)
    # Order can vary for independent tasks, just check all are present
    assert len(sorted_tasks) == 3
    assert {t.id for t in sorted_tasks} == {"A", "B", "C"}

def test_topological_sort_simple_dependencies():
    """Test topological sort with simple linear dependencies."""
    tasks = [
        create_task("A", []),
        create_task("B", ["A"]),
        create_task("C", ["B"])
    ]
    sorted_tasks = topological_sort(tasks)
    assert [t.id for t in sorted_tasks] == ["A", "B", "C"]

def test_topological_sort_complex_dependencies():
    """Test topological sort with branching dependencies."""
    tasks = [
        create_task("A", []),
        create_task("B", ["A"]),
        create_task("C", ["A"]),
        create_task("D", ["B", "C"])
    ]
    sorted_tasks = topological_sort(tasks)
    assert sorted_tasks[0].id == "A"
    # B and C can be in any order after A, before D
    assert (sorted_tasks[1].id == "B" and sorted_tasks[2].id == "C") or \
           (sorted_tasks[1].id == "C" and sorted_tasks[2].id == "B")
    assert sorted_tasks[3].id == "D"

def test_topological_sort_circular_dependency_detection():
    """Test topological sort detects circular dependencies."""
    tasks = [
        create_task("A", ["C"]),
        create_task("B", ["A"]),
        create_task("C", ["B"])
    ]
    with pytest.raises(ValueError, match="Circular dependency detected in tasks."):
        topological_sort(tasks)

def test_detect_cycles_no_cycles():
    """Test detect_cycles with no cycles."""
    tasks = [
        create_task("A", []),
        create_task("B", ["A"]),
        create_task("C", ["B", "A"])
    ]
    assert not detect_cycles(tasks)

def test_detect_cycles_simple_cycle():
    """Test detect_cycles with a simple cycle."""
    tasks = [
        create_task("A", ["B"]),
        create_task("B", ["A"])
    ]
    assert detect_cycles(tasks)

def test_detect_cycles_longer_cycle():
    """Test detect_cycles with a longer cycle."""
    tasks = [
        create_task("A", ["B"]),
        create_task("B", ["C"]),
        create_task("C", ["A"])
    ]
    assert detect_cycles(tasks)

def test_detect_cycles_with_unreachable_tasks():
    """Test detect_cycles with some tasks not part of the main graph."""
    tasks = [
        create_task("A", ["B"]),
        create_task("B", ["C"]),
        create_task("C", ["A"]),
        create_task("D", []),
        create_task("E", ["D"])
    ]
    assert detect_cycles(tasks)

def test_detect_cycles_complex_no_cycle():
    """Test detect_cycles with complex graph but no cycles."""
    tasks = [
        create_task("A", []),
        create_task("B", ["A"]),
        create_task("C", ["A"]),
        create_task("D", ["B", "C"]),
        create_task("E", ["D"])
    ]
    assert not detect_cycles(tasks)

def test_detect_cycles_self_dependency():
    """Test detect_cycles with a task depending on itself."""
    tasks = [
        create_task("A", ["A"])
    ]
    assert detect_cycles(tasks)

def test_topological_sort_with_missing_dependency():
    """Test topological sort handles tasks with dependencies not found in the list."""
    tasks = [
        create_task("A", []),
        create_task("B", ["A", "X"]) # X is missing
    ]
    sorted_tasks = topological_sort(tasks)
    # Tasks with missing dependencies should still be sorted if possible
    # A should come before B
    assert len(sorted_tasks) == 2
    assert sorted_tasks[0].id == "A"
    assert sorted_tasks[1].id == "B"
