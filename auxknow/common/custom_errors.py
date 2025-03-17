from dataclasses import dataclass


@dataclass(frozen=True)
class AuxKnowErrorCodes:
    """Custom Error codes for AuxKnow."""

    SYSTEM_PING_TEST_FAIL_CODE = 101
    SYSTEM_PERPLEXITY_API_KEY_VALIDATION_FAIL_CODE = 102
    SYSTEM_OPENAI_API_KEY_VALIDATION_FAIL_CODE = 103


class AuxKnowException(Exception):
    """Base exception for AuxKnow."""

    def __init__(self, message: str, error_code: int = None):
        self.error_code = error_code
        super().__init__(message)


class AuxKnowMemoryException(AuxKnowException):
    """Base exception class for AuxKnowMemory"""

    pass


class MemoryCapacityError(AuxKnowMemoryException):
    """Raised when memory capacity is exceeded"""

    pass


class SessionClosedError(AuxKnowException):
    """Raised when closed session is accessed."""

    pass
