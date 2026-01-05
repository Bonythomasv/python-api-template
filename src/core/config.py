"""Application configuration management."""
import os
import json
from datetime import datetime, timezone
from typing import List
from src.core.enhanced_logging import get_logger
from src.core.constants import EventKeys

# Try to load dotenv if available (optional dependency)
try:
    from dotenv import load_dotenv  # type: ignore[import-not-found]
    load_dotenv()
except ImportError:
    pass

# Create logger for this module
logger = get_logger(__name__)

# Environment detection
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()

# CORS configuration
ALLOWED_ORIGINS: List[str] = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]

# Debug mode
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# Request size limit configuration
REQUEST_SIZE_LIMIT_KB = float(os.getenv("REQUEST_SIZE_LIMIT_KB", "1024.0"))  # Default 1MB
REQUEST_SIZE_LIMIT_BYTES = int(REQUEST_SIZE_LIMIT_KB * 1024)

# Log rotation configuration
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "0"))  # 0 = keep all backup files forever

def is_local_environment() -> bool:
    """Check if current environment is local development."""
    return ENVIRONMENT == "local"

def is_production_like_environment() -> bool:
    """Check if current environment should enforce production security."""
    return ENVIRONMENT != "local"

def get_environment_security_level() -> str:
    """Get the security level description for the current environment."""
    if ENVIRONMENT == "local":
        return "development_only"
    elif ENVIRONMENT in ["development", "staging", "production"]:
        return "production_like"
    else:
        return "unknown"

def log_environment_variables():
    """Log all loaded environment variables in JSON format."""
    # Get all declared environment variables in this module
    env_vars = {}

    # Get all variables defined at module level
    module_vars = globals()

    # Find all uppercase variables (our environment variables convention)
    for var_name, var_value in module_vars.items():
        if var_name.isupper() and not var_name.startswith("_"):  # Environment variables are uppercase
            # Handle sensitive information
            if any(sensitive in var_name.lower() for sensitive in ['key', 'secret', 'token', 'password', 'auth', 'database']):
                env_vars[f"env.{var_name.lower()}"] = "[SET]" if var_value else "[NOT SET]"
            else:
                # Convert lists to strings for JSON serialization if needed
                if isinstance(var_value, list):
                    var_value = ",".join(str(v) for v in var_value)
                env_vars[f"env.{var_name.lower()}"] = var_value

    # Create the log entry
    log_entry = {
        "@timestamp": datetime.now(timezone.utc).isoformat(),
        "log.level": "info",
        "message": "Application Environment Variables",
        "ecs.version": "1.12.0",
        EventKeys.EVENT_DATASET: "python-api-template"
    }

    # Add all environment variables to the log entry
    log_entry.update(env_vars)

    # Log the environment variables
    logger.info(json.dumps(log_entry, ensure_ascii=False, indent=2))
