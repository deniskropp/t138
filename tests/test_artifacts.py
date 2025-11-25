# tests/test_artifacts.py
import pytest
import os
from unittest.mock import patch, MagicMock
from src.artifacts import ArtifactManager
from src.models import Artifact
from src.paths import get_root_dir, ensure_dir
from src.file_io import read_file, write_file
import uuid

# Mock get_root_dir to use a temporary directory for tests
@pytest.fixture(autouse=True)
def mock_get_root_dir(tmp_path):
    with patch('src.paths.get_root_dir', return_value=str(tmp_path)):
        yield

@pytest.fixture
def clean_artifact_manager():
    """Provides a clean ArtifactManager instance for each test."""
    return ArtifactManager()

def test_artifact_manager_initializes_directory(tmp_path):
    """Test that ArtifactManager creates its artifact directory."""
    manager = ArtifactManager(artifact_dir="my_artifacts")
    expected_path = os.path.join(str(tmp_path), "my_artifacts")
    assert os.path.isdir(expected_path)

def test_store_and_retrieve_text_artifact(clean_artifact_manager):
    """Test storing and retrieving a text artifact."""
    session_id = str(uuid.uuid4())
    artifact_name = "test_output.txt"
    artifact_content = "This is some test output."
    artifact = Artifact(name=artifact_name, type="text", data=artifact_content)

    clean_artifact_manager.store_artifact(artifact, session_id)

    retrieved_artifact = clean_artifact_manager.retrieve_artifact(artifact_name, session_id)
    assert retrieved_artifact is not None
    assert retrieved_artifact.name == artifact_name
    assert retrieved_artifact.type == "text"
    assert retrieved_artifact.data == artifact_content

def test_store_and_retrieve_binary_artifact(clean_artifact_manager):
    """Test storing and retrieving a binary artifact."""
    session_id = str(uuid.uuid4())
    artifact_name = "image.png"
    binary_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82" # Minimal PNG
    artifact = Artifact(name=artifact_name, type="image/png", data=binary_content)

    clean_artifact_manager.store_artifact(artifact, session_id)
    
    # Manually check the file content as retrieve_artifact's stub might not handle binary well yet
    expected_path = os.path.join(get_root_dir(), clean_artifact_manager.artifact_dir, session_id, artifact_name)
    assert os.path.exists(expected_path)
    with open(expected_path, "rb") as f:
        assert f.read() == binary_content

    # Further development will need to make retrieve_artifact handle binary properly
    # For now, it will return str(binary_content)
    retrieved_artifact = clean_artifact_manager.retrieve_artifact(artifact_name, session_id)
    assert retrieved_artifact.data == str(binary_content) # Current limitation of stub

def test_retrieve_non_existent_artifact(clean_artifact_manager):
    """Test retrieving a non-existent artifact returns None."""
    session_id = str(uuid.uuid4())
    assert clean_artifact_manager.retrieve_artifact("non_existent.txt", session_id) is None

def test_get_contextual_artifacts(clean_artifact_manager):
    """Test the placeholder for contextual artifacts."""
    session_id = str(uuid.uuid4())
    context = clean_artifact_manager.get_contextual_artifacts(session_id)
    assert context == {} # Currently an empty dict as per stub
