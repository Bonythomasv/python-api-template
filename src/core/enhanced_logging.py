"""Enhanced logging configuration with duplicate prevention"""
import json
import logging
import logging.handlers
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from src.core.constants import EventKeys

# Registry to track initialized loggers
_LOGGER_REGISTRY = set()
_LOGGER_LOCK = threading.Lock()

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for all log levels."""

    def __init__(self):
        super().__init__()
        self.hostname = "python-api-template"  # Can be made configurable if needed

    def format(self, record: logging.LogRecord) -> str:
        """Format log record into JSON string."""
        # Get the message
        message = record.getMessage()

        # Basic log entry structure
        log_entry = {
            EventKeys.TIMESTAMP: datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            EventKeys.LOG_LEVEL: record.levelname.lower(),
            "message": message,
            "logger.name": record.name,
            EventKeys.ECS_VERSION: "1.12.0",
            EventKeys.EVENT_DATASET: self.hostname,
            "process.pid": record.process,
            "log.logger": record.name,
            "log.origin.file.name": record.filename,
            "log.origin.file.line": record.lineno,
            "log.origin.function": record.funcName
        }

        # Check if message is already JSON
        try:
            if message.startswith('{') and message.endswith('}'):
                message_json = json.loads(message)
                # If message was JSON, use its fields directly
                log_entry.update(message_json)
        except (json.JSONDecodeError, AttributeError):
            pass

        # Add exception info if present
        if record.exc_info:
            exc_type, exc_value, _ = record.exc_info
            if exc_type and exc_value:
                log_entry["error"] = {
                    "type": exc_type.__name__,
                    "message": str(exc_value),
                    "stack_trace": self.formatException(record.exc_info)
                }

        # Add extra fields from the record
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)

        return json.dumps(log_entry, ensure_ascii=False)

class LogConfig:
    def __init__(self, log_dir: Path = Path("logs")):
        """Initialize logging configuration."""
        self.log_dir = log_dir
        # Create directory with proper permissions
        self.log_dir.mkdir(parents=True, exist_ok=True, mode=0o755)

        # Single log file path
        self.log_file = self.log_dir / 'app.log'

        # Configure root logger
        self.setup_root_logger()

    def setup_root_logger(self):
        """Set up the root logger with console and file handlers."""
        # Clear any existing handlers first
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Create handlers
        console_handler = self.get_console_handler(logging.INFO)
        file_handler = self.get_file_handler(self.log_file, logging.INFO)

        # Configure root logger
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

        # Prevent duplicate logging
        root_logger.propagate = False

    def get_console_handler(self, level: int) -> logging.Handler:
        """Get console handler with JSON formatter."""
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(JSONFormatter())
        return handler

    def get_file_handler(self, log_file: Path, level: int) -> logging.Handler:
        """Get rotating file handler with JSON formatter."""
        # Read environment variable directly to avoid circular import
        backup_count = int(os.getenv("LOG_BACKUP_COUNT", "0"))  # 0 = keep all backup files forever
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=backup_count
        )
        handler.setLevel(level)
        handler.setFormatter(JSONFormatter())
        return handler

# Initialize root logger configuration
_log_config = LogConfig()

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Thread-safe logger initialization with duplicate prevention
    """
    with _LOGGER_LOCK:
        logger = logging.getLogger(name)

        if name in _LOGGER_REGISTRY:
            return logger

        # Configure new logger
        logger.setLevel(level)

        # Clear existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Use root logger's handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            logger.addHandler(handler)

        logger.propagate = False

        _LOGGER_REGISTRY.add(name)
        return logger

def shutdown_logging():
    """Properly shutdown all loggers and clean up handlers"""
    with _LOGGER_LOCK:
        for name in _LOGGER_REGISTRY:
            logger = logging.getLogger(name)
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)
        _LOGGER_REGISTRY.clear()
        logging.shutdown()
