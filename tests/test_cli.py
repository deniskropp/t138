# tests/test_cli.py
import pytest
from unittest.mock import patch, MagicMock
from src.cli import main_cli
import sys

@pytest.fixture(autouse=True)
def mock_cli_dependencies(monkeypatch):
    """Mock external dependencies for CLI."""
    monkeypatch.setattr('src.bootstrap.bootstrap_system', MagicMock())
    monkeypatch.setattr('src.logger.setup_logging', MagicMock())
    monkeypatch.setattr('src.paths.get_root_dir', lambda: '/mock/root')
    monkeypatch.setattr('print', MagicMock()) # Mock print to capture output

@pytest.fixture
def run_cli():
    """Helper to run main_cli with given arguments."""
    def _run_cli(args):
        with patch.object(sys, 'argv', ['cli_script.py'] + args):
            main_cli()
    return _run_cli

def test_run_command(run_cli, mock_cli_dependencies):
    """Test the 'run' command."""
    run_cli(["run", "workflow_file.yaml"])
    mock_cli_dependencies['print'].assert_called_with("Running workflow: workflow_file.yaml")
    # Further assertions would involve mocking the orchestrator call

def test_init_command(run_cli, mock_cli_dependencies):
    """Test the 'init' command."""
    run_cli(["init"])
    mock_cli_dependencies['print'].assert_called_with("Initializing new project...")
    # Further assertions would involve mocking the project initialization logic

def test_status_command(run_cli, mock_cli_dependencies):
    """Test the 'status' command."""
    run_cli(["status"])
    mock_cli_dependencies['print'].assert_called_with("Showing system status...")
    # Further assertions would involve mocking the status display logic

def test_no_command(run_cli, mock_cli_dependencies):
    """Test running cli with no command (should print help)."""
    run_cli([])
    mock_cli_dependencies['print'].assert_called() # Should print help message
    # Cannot easily assert specific help message content without parsing it

def test_unknown_command(run_cli, mock_cli_dependencies):
    """Test running cli with an unknown command."""
    with pytest.raises(SystemExit): # argparse exits on unknown command
        run_cli(["unknown_cmd"])
