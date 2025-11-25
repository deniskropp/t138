# tests/test_logger.py
import pytest
import logging
import os
from unittest.mock import patch, MagicMock
from src.logger import setup_logging, ColoredFormatter, JsonFormatter
from src.config import settings
from src.paths import get_root_dir

# Mock get_root_dir to use a temporary directory for tests
@pytest.fixture(autouse=True)
def mock_get_root_dir(tmp_path):
    with patch('src.paths.get_root_dir', return_value=str(tmp_path)):
        yield

@pytest.fixture
def clean_logger():
    # Remove all handlers from the root logger before each test
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)
    yield
    # Clean up again after the test
    for handler in logging.getLogger().handlers[:]:
        logging.getLogger().removeHandler(handler)

def test_setup_logging_initializes_handlers(clean_logger):
    """Test that setup_logging adds the correct number and types of handlers."""
    setup_logging()
    handlers = logging.getLogger().handlers
    assert len(handlers) == 3 # Stream, File, JSON File

    assert any(isinstance(h, logging.StreamHandler) for h in handlers)
    assert any(isinstance(h, logging.FileHandler) for h in handlers)
    
    # Check for specific formatter types as an indirect way to verify JSON file handler
    file_handlers = [h for h in handlers if isinstance(h, logging.FileHandler)]
    assert any(isinstance(h.formatter, JsonFormatter) for h in file_handlers)
    assert any(isinstance(h.formatter, logging.Formatter) and not isinstance(h.formatter, (ColoredFormatter, JsonFormatter)) for h in file_handlers)


def test_colored_formatter():
    """Test ColoredFormatter applies colors correctly."""
    formatter = ColoredFormatter("%(levelname)s: %(message)s")
    record = logging.LogRecord("test", logging.INFO, __file__, 1, "Test message", [], None)
    
    formatted_message = formatter.format(record)
    assert "\033[92mINFO: Test message\033[0m" in formatted_message # Green for INFO

    record.levelname = "WARNING"
    formatted_message = formatter.format(record)
    assert "\033[93mWARNING: Test message\033[0m" in formatted_message # Yellow for WARNING

def test_json_formatter():
    """Test JsonFormatter outputs valid JSON."""
    formatter = JsonFormatter()
    record = logging.LogRecord("test", logging.INFO, __file__, 1, "Test message", [], None)
    
    formatted_message = formatter.format(record)
    data = json.loads(formatted_message) # Should be valid JSON
    assert data["level"] == "INFO"
    assert data["message"] == "Test message"
    assert "timestamp" in data

def test_logging_level_from_config(clean_logger, monkeypatch):
    """Test that the logging level is set from settings."""
    monkeypatch.setattr(settings, "LOG_LEVEL", "DEBUG")
    setup_logging()
    assert logging.getLogger().level == logging.DEBUG
    
    # Test with a different level
    clean_logger # Reset handlers
    monkeypatch.setattr(settings, "LOG_LEVEL", "WARNING")
    setup_logging()
    assert logging.getLogger().level == logging.WARNING
