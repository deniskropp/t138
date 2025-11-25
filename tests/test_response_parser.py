# tests/test_response_parser.py
import pytest
import json
from src.response_parser import parse_response

def test_parse_response_valid_json():
    """Test parsing a valid JSON string."""
    json_string = '{"status": "success", "data": {"key": "value"}}'
    expected_output = {"status": "success", "data": {"key": "value"}}
    assert parse_response(json_string) == expected_output

def test_parse_response_invalid_json_fallback_to_text():
    """Test parsing an invalid JSON string falls back to text."""
    plain_text = "This is a plain text response."
    expected_output = {"output": plain_text, "status": "success", "artifacts": []}
    assert parse_response(plain_text) == expected_output

def test_parse_response_empty_string_fallback_to_text():
    """Test parsing an empty string falls back to text."""
    empty_string = ""
    expected_output = {"output": empty_string, "status": "success", "artifacts": []}
    assert parse_response(empty_string) == expected_output

def test_parse_response_json_with_different_types():
    """Test parsing JSON with various data types."""
    json_string = '{"number": 123, "boolean": true, "list": [1, 2, 3]}'
    expected_output = {"number": 123, "boolean": True, "list": [1, 2, 3]}
    assert parse_response(json_string) == expected_output

def test_parse_response_malformed_json_fallback_to_text():
    """Test parsing malformed JSON (e.g., missing quotes) falls back to text."""
    malformed_json = '{status: "success"}' # Missing quotes around 'status'
    expected_output = {"output": malformed_json, "status": "success", "artifacts": []}
    assert parse_response(malformed_json) == expected_output
