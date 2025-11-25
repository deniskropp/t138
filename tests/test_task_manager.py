# tests/test_task_manager.py
import pytest
from src.task_manager import TaskQueue
from src.models import TaskSpec
import uuid

@pytest.fixture
def clean_task_queue():
    """Provides a clean TaskQueue instance for each test."""
    return TaskQueue()

def test_add_task(clean_task_queue):
    """Test adding a single task to the queue."""
    task_id = str(uuid.uuid4())
    task = TaskSpec(id=task_id, name="TestTask", description="Desc", agent_name="AgentA")
    clean_task_queue.add_task(task)
    assert clean_task_queue.get_task_status(task_id) == "pending"
    assert not clean_task_queue._queue.empty() # Accessing internal for assertion here

def test_get_next_task(clean_task_queue):
    """Test retrieving the next task and its status update."""
    task1_id = str(uuid.uuid4())
    task2_id = str(uuid.uuid4())
    task1 = TaskSpec(id=task1_id, name="Task1", description="Desc1", agent_name="AgentA")
    task2 = TaskSpec(id=task2_id, name="Task2", description="Desc2", agent_name="AgentB")

    clean_task_queue.add_task(task1)
    clean_task_queue.add_task(task2)

    retrieved_task = clean_task_queue.get_next_task()
    assert retrieved_task.id == task1_id
    assert clean_task_queue.get_task_status(task1_id) == "in_progress"
    assert clean_task_queue.get_task_status(task2_id) == "pending"

    retrieved_task_2 = clean_task_queue.get_next_task()
    assert retrieved_task_2.id == task2_id
    assert clean_task_queue.get_task_status(task2_id) == "in_progress"

def test_get_next_task_empty_queue(clean_task_queue):
    """Test getting next task from an empty queue."""
    assert clean_task_queue.get_next_task() is None

def test_update_task_status(clean_task_queue):
    """Test updating the status of a task."""
    task_id = str(uuid.uuid4())
    task = TaskSpec(id=task_id, name="TestTask", description="Desc", agent_name="AgentA")
    clean_task_queue.add_task(task)
    
    clean_task_queue.get_next_task() # Status becomes 'in_progress'
    clean_task_queue.update_task_status(task_id, "completed")
    assert clean_task_queue.get_task_status(task_id) == "completed"

    clean_task_queue.update_task_status("non_existent_task", "failed") # Should not error
    assert clean_task_queue.get_task_status("non_existent_task") is None

def test_get_task_status(clean_task_queue):
    """Test retrieving task status."""
    task_id = str(uuid.uuid4())
    task = TaskSpec(id=task_id, name="TestTask", description="Desc", agent_name="AgentA")
    clean_task_queue.add_task(task)
    assert clean_task_queue.get_task_status(task_id) == "pending"
    clean_task_queue.get_next_task()
    assert clean_task_queue.get_task_status(task_id) == "in_progress"
    clean_task_queue.update_task_status(task_id, "failed")
    assert clean_task_queue.get_task_status(task_id) == "failed"
