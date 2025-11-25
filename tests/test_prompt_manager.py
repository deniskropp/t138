# tests/test_prompt_manager.py
import pytest
import os
from unittest.mock import patch, MagicMock
from src.prompt_manager import PromptManager
from src.paths import get_root_dir
from src.config import settings

# Mock get_root_dir to use a temporary directory for tests
@pytest.fixture(autouse=True)
def mock_get_root_dir(tmp_path):
    with patch('src.paths.get_root_dir', return_value=str(tmp_path)):
        yield

@pytest.fixture
def create_test_prompts(tmp_path):
    """Fixture to create dummy prompt files in a temporary prompts directory."""
    prompts_dir = os.path.join(str(tmp_path), settings.PROMPTS_DIR)
    os.makedirs(prompts_dir, exist_ok=True)
    
    with open(os.path.join(prompts_dir, "welcome.txt"), "w") as f:
        f.write("Welcome, {name}!")
    with open(os.path.join(prompts_dir, "farewell.txt"), "w") as f:
        f.write("Goodbye!")
    
    return prompts_dir

def test_prompt_manager_loads_prompts(create_test_prompts):
    """Test that PromptManager loads prompt files correctly."""
    manager = PromptManager()
    assert "welcome" in manager.prompts
    assert manager.get_prompt("welcome") == "Welcome, {name}!"
    assert "farewell" in manager.prompts
    assert manager.get_prompt("farewell") == "Goodbye!"

def test_prompt_manager_get_nonexistent_prompt():
    """Test retrieving a prompt that does not exist."""
    manager = PromptManager()
    assert manager.get_prompt("non_existent") == ""

def test_prompt_manager_update_prompt():
    """Test updating a prompt in memory."""
    manager = PromptManager()
    original_prompt = manager.get_prompt("welcome")
    new_content = "Hello, {name}! Updated!"
    manager.update_prompt("welcome", new_content)
    assert manager.get_prompt("welcome") == new_content
    assert original_prompt != new_content

def test_prompt_manager_handles_empty_prompts_dir(tmp_path):
    """Test PromptManager behavior with an empty prompts directory."""
    empty_prompts_dir = os.path.join(str(tmp_path), "empty_prompts")
    os.makedirs(empty_prompts_dir)
    manager = PromptManager(prompt_dir="empty_prompts")
    assert manager.prompts == {}
    assert manager.get_prompt("any") == ""
