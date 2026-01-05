"""Main FastAPI application entry point."""
import json
import atexit
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.core.enhanced_logging import get_logger, shutdown_logging
from src.core.config import (
    ALLOWED_ORIGINS,
    DEBUG_MODE,
    ENVIRONMENT,
    log_environment_variables
)
from src.core.constants import EventKeys, MediaTypes

# Initialize logger
logger = get_logger(__name__)

# Define a data model for input if needed (for demonstration purposes)
class InputModel(BaseModel):
    nums: List[int]

class PythonAPITemplate:
    """Encapsulates the Python API Template in an object-oriented structure."""

    ENV = ENVIRONMENT
    # Enable docs only in dev/local
    enable_docs = ENV in ["dev", "local", "development"]

    def __init__(self):
        """Initialize the FastAPI application and configure settings."""
        self.app = FastAPI(
            title="Python API Template",
            description="A demonstration of the Make Python Devex concept project",
            version="0.0.1",
            docs_url="/docs" if self.enable_docs else None,
            redoc_url="/redoc" if self.enable_docs else None,
            openapi_url="/openapi.json" if self.enable_docs else None,
        )

        self._add_middlewares()
        self._register_routes()

        # Register startup and shutdown events
        @self.app.on_event("startup")
        async def startup_event():
            await self._on_startup()

        @self.app.on_event("shutdown")
        async def shutdown_event():
            await self._on_shutdown()

        # Register cleanup
        atexit.register(shutdown_logging)

    def _add_middlewares(self):
        """Attach middlewares to the FastAPI application."""
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=ALLOWED_ORIGINS if "*" not in ALLOWED_ORIGINS else ["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            allow_headers=["*"],
            expose_headers=["*"],
            max_age=600,  # Cache preflight requests for 10 minutes
        )

        # Add request logging middleware
        self.app.middleware("http")(self._log_requests)

    def _register_routes(self):
        """Include all API routes."""
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {"message": "Welcome to Python API Template"}

        @self.app.get("/hello")
        async def hello_user(name: str):
            """
            Greet the user with their name provided as a query parameter.
            """
            logger.info(f"Received input: {name}")
            return {"message": f"Hello, {name}!"}

        @self.app.get("/sum")
        async def sum_numbers(a: int, b: int):
            """
            Sum two numbers provided as query parameters.
            """
            logger.info(f"Summing {a} and {b}")
            return {"sum": a + b}

        @self.app.post("/sum-list")
        async def sum_list_endpoint(input_model: InputModel):
            """
            Sum a list of numbers provided in the request body.
            """
            result = sum(input_model.nums)
            logger.info(f"Summing list: {input_model.nums} = {result}")
            return {"sum": result}

    async def _log_requests(self, request: Request, call_next):
        """Middleware to log incoming requests and responses."""
        request_id = str(uuid.uuid4())
        start_time = datetime.now(timezone.utc)

        # Extract client IP
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        client_ip = "Unknown"
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0]
        elif request.client and request.client.host:
            client_ip = request.client.host

        # Log incoming request
        log_entry = {
            EventKeys.TIMESTAMP: start_time.isoformat(),
            EventKeys.LOG_LEVEL: "info",
            "message": "Incoming request",
            EventKeys.ECS_VERSION: EventKeys.ECS_CURRENT_VERSION,
            EventKeys.EVENT_DATASET: EventKeys.APP_NAME,
            "trace.id": request_id,
            "http.request.method": request.method,
            "url.path": request.url.path,
            "url.query": dict(request.query_params) if request.query_params else {},
            "client.ip": client_ip,
            "user_agent.original": request.headers.get("User-Agent", "Unknown"),
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False, indent=2))

        # Process request
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        # Calculate duration
        end_time = datetime.now(timezone.utc)
        duration = (end_time - start_time).total_seconds()

        # Log response
        log_entry = {
            EventKeys.TIMESTAMP: end_time.isoformat(),
            EventKeys.LOG_LEVEL: "info",
            "message": "Response sent",
            EventKeys.ECS_VERSION: EventKeys.ECS_CURRENT_VERSION,
            EventKeys.EVENT_DATASET: EventKeys.APP_NAME,
            "trace.id": request_id,
            "http.response.status_code": response.status_code,
            "request_duration_seconds": duration,
        }
        logger.info(json.dumps(log_entry, ensure_ascii=False, indent=2))

        return response

    async def _on_startup(self):
        """Event hook triggered when the API starts."""
        # Log environment variables
        log_environment_variables()

        logger.info(json.dumps({
            EventKeys.TIMESTAMP: datetime.now(timezone.utc).isoformat(),
            EventKeys.LOG_LEVEL: "info",
            "message": "Python API Template has started successfully.",
            EventKeys.ECS_VERSION: EventKeys.ECS_CURRENT_VERSION,
            EventKeys.EVENT_DATASET: EventKeys.APP_NAME
        }, ensure_ascii=False, indent=2))

    async def _on_shutdown(self):
        """Event hook triggered when the API shuts down."""
        logger.info(json.dumps({
            EventKeys.TIMESTAMP: datetime.now(timezone.utc).isoformat(),
            EventKeys.LOG_LEVEL: "info",
            "message": "Python API Template is shutting down.",
            EventKeys.ECS_VERSION: EventKeys.ECS_CURRENT_VERSION,
            EventKeys.EVENT_DATASET: EventKeys.APP_NAME
        }, ensure_ascii=False, indent=2))

# Standalone function (for backward compatibility)
def sum_list(nums: List[int]) -> int:
    """Sum a list of numbers."""
    return sum(nums)

# Main function (for backward compatibility)
def main() -> None:
    """Main entry point for standalone execution."""
    logger.info("Starting")
    result = sum_list([1, 2])
    logger.info(f"Got {result}")
    atexit.register(lambda: logger.info("Exiting!"))

# Instantiate and expose the FastAPI app
python_api_template = PythonAPITemplate()
app = python_api_template.app

# Add validation exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with security logging."""
    # Extract client IP for security monitoring
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    client_ip = "Unknown"
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    elif request.client and request.client.host:
        client_ip = request.client.host

    # Log validation failures with client IP for security monitoring
    logger.warning(
        f"Validation failed for {request.method} {request.url.path} from {client_ip}",
        extra={
            "client_ip": client_ip,
            "method": request.method,
            "path": request.url.path,
            "validation_errors": exc.errors()
        }
    )

    # Return standardized error response
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "message": "Validation failed",
            "status_code": 422
        }
    )
