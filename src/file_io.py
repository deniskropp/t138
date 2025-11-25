# src/file_io.py
"""Utility functions for file input/output operations."""
import logging

logger = logging.getLogger(__name__)

def read_file(path: str, mode: str = 'r', encoding: str = 'utf-8') -> str | bytes | None:
    """
    Reads content from a file.
    Supports text ('r') and binary ('rb') modes.
    Returns None on error.
    """
    try:
        if 'b' in mode:
            with open(path, mode) as f:
                return f.read()
        else:
            with open(path, mode, encoding=encoding) as f:
                return f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        return None
    except IOError as e:
        logger.error(f"Error reading file {path}: {e}")
        return None

def write_file(path: str, content: str | bytes, mode: str = 'w', encoding: str = 'utf-8') -> bool:
    """
    Writes content to a file.
    Supports text ('w', 'a') and binary ('wb', 'ab') modes.
    Returns True on success, False on error.
    """
    try:
        if 'b' in mode:
            if not isinstance(content, bytes):
                logger.error(f"Content must be bytes for binary write mode '{mode}': {path}")
                return False
            with open(path, mode) as f:
                f.write(content)
        else:
            if not isinstance(content, str):
                logger.error(f"Content must be string for text write mode '{mode}': {path}")
                return False
            with open(path, mode, encoding=encoding) as f:
                f.write(content)
        return True
    except IOError as e:
        logger.error(f"Error writing to file {path}: {e}")
        return False
