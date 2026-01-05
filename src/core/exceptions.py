"""Custom exception classes for the application."""
from typing import Any, Dict, Optional
from fastapi import HTTPException
from pydantic import BaseModel

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class APIError(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail=ErrorDetail(
                code=code,
                message=message,
                details=details
            ).dict()
        )

class ValidationError(APIError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=400,
            code='VALIDATION_ERROR',
            message=message,
            details=details
        )

class AuthenticationError(APIError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=401,
            code='AUTHENTICATION_ERROR',
            message=message,
            details=details
        )

class AuthorizationError(APIError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=403,
            code='AUTHORIZATION_ERROR',
            message=message,
            details=details
        )

class ResourceNotFoundError(APIError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=404,
            code='RESOURCE_NOT_FOUND',
            message=message,
            details=details
        )

class InternalServerError(APIError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=500,
            code='INTERNAL_SERVER_ERROR',
            message=message,
            details=details
        )
