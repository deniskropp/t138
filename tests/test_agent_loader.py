# tests/test_agent_loader.py
import pytest
import os
import yaml
import json
from unittest.mock import patch
from src.agent_loader import load_agent_specs
from src.models import AgentSpec
from src.paths import get_root_dir

# Mock get_root_dir to use a temporary directory for tests
@pytest.fixture(autouse=True)
def mock_get_root_dir(tmp_path):
    with patch('src.paths.get_root_dir', return_value=str(tmp_path)):
        yield

@pytest.fixture
def create_test_agent_specs(tmp_path):
    """Fixture to create dummy agent spec files in a temporary directory."""
    spec_dir = os.path.join(str(tmp_path), "agents", "specs")
    os.makedirs(spec_dir, exist_ok=True)
    
    # Create a YAML spec file
    yaml_content = {
        "name": "YAML_Agent",
        "role": "YamlProcessor",
        "description": "An agent that processes YAML files."
    }
    with open(os.path.join(spec_dir, "yaml_agent.yaml"), "w") as f:
        yaml.dump(yaml_content, f)

    # Create a JSON spec file
    json_content = {
        "name": "JSON_Agent",
        "role": "JsonProcessor",
        "description": "An agent that processes JSON files."
    }
    with open(os.path.join(spec_dir, "json_agent.json"), "w") as f:
        json.dump(json_content, f)
    
    # Create an invalid file
    with open(os.path.join(spec_dir, "invalid.txt"), "w") as f:
        f.write("This is not a valid spec.")
    
    return spec_dir

def test_load_agent_specs_success(create_test_agent_specs):
    """Test that agent specifications are loaded and parsed correctly."""
    specs = load_agent_specs()
    assert len(specs) == 2
    
    yaml_agent = next(s for s in specs if s.name == "YAML_Agent")
    assert yaml_agent.role == "YamlProcessor"
    assert yaml_agent.description == "An agent that processes YAML files."

    json_agent = next(s for s in specs if s.name == "JSON_Agent")
    assert json_agent.role == "JsonProcessor"
    assert json_agent.description == "An agent that processes JSON files."

def test_load_agent_specs_empty_dir():
    """Test loading from an empty or non-existent directory."""
    specs = load_agent_specs(spec_dir="non_existent_dir")
    assert len(specs) == 0

def test_load_agent_specs_invalid_file(create_test_agent_specs, caplog):
    """Test handling of invalid spec files."""
    with caplog.at_level(logging.ERROR):
        specs = load_agent_specs()
        assert "Error parsing agent spec file" in caplog.text
