# tests/test_paths.py
import pytest
import os
from src.paths import get_root_dir, ensure_dir

def test_get_root_dir():
    """Test that get_root_dir correctly identifies the project root."""
    # This test assumes 'main.py' is at the project root.
    # We create a dummy main.py for testing purposes within a temporary directory.
    temp_root = "/tmp/test_project_root"
    temp_src = os.path.join(temp_root, "src")
    os.makedirs(temp_src, exist_ok=True)
    with open(os.path.join(temp_root, "main.py"), "w") as f:
        f.write("# dummy main.py")
    
    # Mock the os.path.abspath(__file__) for src/paths.py to be within the temp_src
    original_abspath = os.path.abspath
    def mock_abspath(path):
        if path.endswith("paths.py"):
            return os.path.join(temp_src, "paths.py")
        return original_abspath(path)
    
    with pytest.MonkeyPatch().context() as m:
        m.setattr(os.path, "abspath", mock_abspath)
        # Re-import get_root_dir to use the mocked abspath
        from src.paths import get_root_dir as reloaded_get_root_dir
        assert reloaded_get_root_dir() == temp_root
    
    # Clean up dummy files
    os.remove(os.path.join(temp_root, "main.py"))
    os.rmdir(temp_src)
    os.rmdir(temp_root)


def test_ensure_dir(tmp_path):
    """Test that ensure_dir creates a directory if it doesn't exist."""
    test_dir = tmp_path / "new_dir"
    assert not test_dir.exists()
    ensure_dir(str(test_dir))
    assert test_dir.is_dir()

def test_ensure_dir_existing(tmp_path):
    """Test that ensure_dir does nothing if the directory already exists."""
    test_dir = tmp_path / "existing_dir"
    test_dir.mkdir()
    assert test_dir.is_dir()
    ensure_dir(str(test_dir))
    assert test_dir.is_dir()
