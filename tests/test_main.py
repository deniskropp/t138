# tests/test_main.py
import pytest
from unittest.mock import patch, MagicMock
import sys
from src.bootstrap import bootstrap_system
from src.cli import main_cli
from src.runtime import system_runtime
import logging

@pytest.fixture(autouse=True)
def mock_main_dependencies(monkeypatch):
    """Mock dependencies for main.py."""
    monkeypatch.setattr('src.bootstrap.bootstrap_system', MagicMock())
    monkeypatch.setattr('src.cli.main_cli', MagicMock())
    monkeypatch.setattr('logging.info', MagicMock()) # Mock logging for cleaner output

def test_main_function_calls_bootstrap_and_cli():
    """Test that the main function correctly calls bootstrap and cli functions."""
    from main import main # Import here to ensure mocks are active

    main()

    src.bootstrap.bootstrap_system.assert_called_once()
    src.cli.main_cli.assert_called_once()
    logging.info.assert_any_call("Starting application...")
    logging.info.assert_any_call("Application finished.")

def test_main_entry_point_behavior(mock_main_dependencies):
    """Test the __name__ == '__main__' block behavior."""
    # Simulate running main.py directly
    with patch.object(sys, 'argv', ['main.py']):
        with patch('main.main') as mock_main_func:
            # Import main again to trigger the __name__ == '__main__' block
            # This is a common pattern for testing main functions
            import runpy
            runpy.run_module('main', run_name='__main__')
            mock_main_func.assert_called_once()
