# src/logger.py
"""Application-wide logging setup and configuration."""
import logging
import os
from src.paths import get_root_dir, ensure_dir
from src.config import settings
import json

class ColoredFormatter(logging.Formatter):
    COLORS = {
        "WARNING": "\033[93m",  # Yellow
        "INFO": "\033[92m",     # Green
        "DEBUG": "\033[94m",    # Blue
        "CRITICAL": "\033[95m", # Magenta
        "ERROR": "\033[91m",    # Red
        "RESET": "\033[0m",     # Reset
    }

    def format(self, record):
        log_message = super().format(record)
        return f"{self.COLORS.get(record.levelname, self.COLORS['RESET'])}{log_message}{self.COLORS['RESET']}"

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
            "process": record.process,
            "thread": record.thread
        }
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def setup_logging():
    """Sets up comprehensive logging configuration."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logging.getLogger().setLevel(log_level)

    log_dir = os.path.join(get_root_dir(), "logs")
    ensure_dir(log_dir)

    # Console handler with colored output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(console_handler)

    # File handler with standard text format
    file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(file_handler)

    # JSON file handler
    json_handler = logging.FileHandler(os.path.join(log_dir, "app.json"))
    json_handler.setFormatter(JsonFormatter())
    logging.getLogger().addHandler(json_handler)

    logging.info(f"Logging configured with level: {settings.LOG_LEVEL}")
