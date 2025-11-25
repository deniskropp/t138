# src/context.py
"""Manages the execution context, including environment variables and session data."""
from typing import Dict, Any
from src.models import ExecutionContext

class ContextManager:
    def __init__(self):
        self._context: ExecutionContext = ExecutionContext(session_id="default")

    def set_context(self, context: ExecutionContext):
        """Sets the current execution context."""
        self._context = context

    def get_context(self) -> ExecutionContext:
        """Returns the current execution context."""
        return self._context

    def update_env_var(self, key: str, value: str):
        """Updates an environment variable in the context."""
        self._context.env_vars[key] = value

    def update_runtime_flag(self, key: str, value: Any):
        """Updates a runtime flag in the context."""
        self._context.runtime_flags[key] = value

context_manager = ContextManager()
