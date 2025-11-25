# src/paths.py
"""Utility functions for managing file paths and directories."""
import os

def get_root_dir() -> str:
    """
    Returns the project root directory.
    Assumes 'main.py' is in the root directory.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    while current_dir != os.path.dirname(current_dir): # Prevent infinite loop at system root
        if os.path.exists(os.path.join(current_dir, 'main.py')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")) # Fallback

def ensure_dir(path: str):
    """Ensures that a directory exists, creating it if necessary."""
    os.makedirs(path, exist_ok=True)
