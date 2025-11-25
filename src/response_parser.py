# src/response_parser.py
"""Handles parsing and deserialization of various response formats (e.g., JSON, plain text)."""
import json
from typing import Any, Dict
from src.models import AgentResponse # Assuming AgentResponse is the target model

def parse_response(response_text: str) -> Dict[str, Any]:
    """
    Parses a response string, attempting JSON deserialization first,
    then falling back to plain text.
    """
    try:
        data = json.loads(response_text)
        # Optional: Validate against AgentResponse schema here
        return data
    except json.JSONDecodeError:
        return {"output": response_text, "status": "success", "artifacts": []}
