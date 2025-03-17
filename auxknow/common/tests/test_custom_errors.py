from auxknow.common.custom_errors import (
    AuxKnowErrorCodes,
    AuxKnowException,
    AuxKnowMemoryException,
    MemoryCapacityError,
    SessionClosedError,
)


def test_error_codes():
    """Test all error codes are defined correctly."""
    assert AuxKnowErrorCodes.SYSTEM_PING_TEST_FAIL_CODE == 101
    assert AuxKnowErrorCodes.SYSTEM_PERPLEXITY_API_KEY_VALIDATION_FAIL_CODE == 102
    assert AuxKnowErrorCodes.SYSTEM_OPENAI_API_KEY_VALIDATION_FAIL_CODE == 103


def test_auxknow_exception():
    """Test AuxKnowException base class."""
    try:
        raise AuxKnowException("Test error")
    except AuxKnowException as e:
        assert str(e) == "Test error"
        assert isinstance(e, Exception)


def test_auxknow_memory_exception():
    """Test AuxKnowMemoryException class."""
    try:
        raise AuxKnowMemoryException("Memory error")
    except AuxKnowMemoryException as e:
        assert str(e) == "Memory error"
        assert isinstance(e, AuxKnowException)
        assert isinstance(e, Exception)


def test_memory_capacity_error():
    """Test MemoryCapacityError class."""
    try:
        raise MemoryCapacityError("Memory capacity exceeded")
    except MemoryCapacityError as e:
        assert str(e) == "Memory capacity exceeded"
        assert isinstance(e, AuxKnowMemoryException)
        assert isinstance(e, AuxKnowException)
        assert isinstance(e, Exception)


def test_session_closed_error():
    """Test SessionClosedError class."""
    try:
        raise SessionClosedError("Session is closed")
    except SessionClosedError as e:
        assert str(e) == "Session is closed"
        assert isinstance(e, AuxKnowException)
        assert isinstance(e, Exception)


def test_error_codes_immutability():
    """Test that AuxKnowErrorCodes is immutable."""
    error_codes = AuxKnowErrorCodes()
    try:
        error_codes.SYSTEM_PING_TEST_FAIL_CODE = 999
        assert False, "Should not be able to modify frozen dataclass"
    except AttributeError:
        assert True


def test_auxknow_exception_with_code():
    """Test AuxKnowException with error code."""
    try:
        raise AuxKnowException(
            "Test error", AuxKnowErrorCodes.SYSTEM_PING_TEST_FAIL_CODE
        )
    except AuxKnowException as e:
        assert str(e) == "Test error"
        assert isinstance(e, Exception)
        assert e.error_code == AuxKnowErrorCodes.SYSTEM_PING_TEST_FAIL_CODE


def test_auxknow_memory_exception_with_code():
    """Test AuxKnowMemoryException with error code."""
    try:
        raise AuxKnowMemoryException(
            "Memory error", AuxKnowErrorCodes.SYSTEM_PING_TEST_FAIL_CODE
        )
    except AuxKnowMemoryException as e:
        assert str(e) == "Memory error"
        assert isinstance(e, AuxKnowException)
        assert isinstance(e, Exception)
        assert e.error_code == AuxKnowErrorCodes.SYSTEM_PING_TEST_FAIL_CODE


def test_memory_capacity_error_with_code():
    """Test MemoryCapacityError with error code."""
    try:
        raise MemoryCapacityError(
            "Memory capacity exceeded", AuxKnowErrorCodes.SYSTEM_PING_TEST_FAIL_CODE
        )
    except MemoryCapacityError as e:
        assert str(e) == "Memory capacity exceeded"
        assert isinstance(e, AuxKnowMemoryException)
        assert isinstance(e, AuxKnowException)
        assert isinstance(e, Exception)
        assert e.error_code == AuxKnowErrorCodes.SYSTEM_PING_TEST_FAIL_CODE


def test_session_closed_error_with_code():
    """Test SessionClosedError with error code."""
    try:
        raise SessionClosedError(
            "Session is closed", AuxKnowErrorCodes.SYSTEM_PING_TEST_FAIL_CODE
        )
    except SessionClosedError as e:
        assert str(e) == "Session is closed"
        assert isinstance(e, AuxKnowException)
        assert isinstance(e, Exception)
        assert e.error_code == AuxKnowErrorCodes.SYSTEM_PING_TEST_FAIL_CODE
