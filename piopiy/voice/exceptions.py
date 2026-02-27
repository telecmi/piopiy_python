"""Custom exception types for the Piopiy SDK."""

from typing import Any, Dict, Optional


class PiopiyError(Exception):
    """Base exception for all SDK errors."""


class PiopiyValidationError(PiopiyError):
    """Raised when a request payload fails client-side validation."""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message)
        self.field = field


class PiopiyNetworkError(PiopiyError):
    """Raised when network-level issues occur."""

    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(message)
        self.original_exception = original_exception


class PiopiyAPIError(PiopiyError):
    """Raised when the Piopiy API responds with a non-2xx status code."""

    def __init__(self, message: str, status_code: int, payload: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload or {}
