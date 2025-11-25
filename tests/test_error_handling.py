# tests/test_error_handling.py
import pytest
import logging
import time
from unittest.mock import MagicMock, patch
from src.error_handling import handle_exception, retry_policy

@pytest.fixture(autouse=True)
def mock_logger_for_error_handling(monkeypatch):
    """Mock the logger to capture log messages."""
    mock_log = MagicMock()
    monkeypatch.setattr('src.error_handling.logger', mock_log)
    monkeypatch.setattr('logging.getLogger', MagicMock(return_value=mock_log))
    return mock_log

def test_handle_exception_decorator_logs_and_reraises(mock_logger_for_error_handling):
    """Test handle_exception logs the error and re-raises it."""
    @handle_exception
    def faulty_function():
        raise ValueError("Something went wrong!")

    with pytest.raises(ValueError, match="Something went wrong!"):
        faulty_function()
    
    mock_logger_for_error_handling.error.assert_called_once()
    assert "Error in faulty_function: Something went wrong!" in mock_logger_for_error_handling.error.call_args[0][0]

def test_handle_exception_decorator_no_exception():
    """Test handle_exception works fine when no exception occurs."""
    @handle_exception
    def successful_function():
        return "Success"

    assert successful_function() == "Success"

def test_retry_policy_decorator_succeeds_on_retry(mock_logger_for_error_handling):
    """Test retry_policy succeeds after a few retries."""
    mock_func = MagicMock(side_effect=[ValueError("Attempt 1"), ValueError("Attempt 2"), "Success"])

    @retry_policy(retries=3, delay=0.01)
    def flappy_function():
        return mock_func()
    
    assert flappy_function() == "Success"
    assert mock_func.call_count == 3
    assert mock_logger_for_error_handling.warning.call_count == 2 # Two warnings for two failures

def test_retry_policy_decorator_fails_after_max_retries(mock_logger_for_error_handling):
    """Test retry_policy fails after maximum retries."""
    mock_func = MagicMock(side_effect=[ValueError("Attempt 1"), ValueError("Attempt 2"), ValueError("Attempt 3")])

    @retry_policy(retries=2, delay=0.01) # Only 2 retries, total 3 attempts
    def very_flappy_function():
        return mock_func()

    with pytest.raises(Exception, match="Function very_flappy_function failed after 2 attempts."):
        very_flappy_function()
    
    assert mock_func.call_count == 2 # Original call + 1 retry
    assert mock_logger_for_error_handling.warning.call_count == 1 # One warning for the first failure

def test_retry_policy_decorator_no_retries_needed():
    """Test retry_policy works if no retries are needed."""
    mock_func = MagicMock(return_value="Instant Success")

    @retry_policy(retries=3, delay=0.01)
    def instant_success_function():
        return mock_func()

    assert instant_success_function() == "Instant Success"
    assert mock_func.call_count == 1
