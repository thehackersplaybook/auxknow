from functools import wraps
import time
from typing import Any, Callable, TypeVar, ParamSpec, cast
from .printer import Printer
from enum import Enum

P = ParamSpec("P")
R = TypeVar("R")


class TimeUnit(Enum):
    """Time units for performance logging"""

    NANOSECONDS = "ns"
    MICROSECONDS = "µs"
    MILLISECONDS = "ms"
    SECONDS = "s"


def _convert_time(seconds: float, unit: TimeUnit) -> float:
    """Convert time from seconds to specified unit"""
    conversions = {
        TimeUnit.NANOSECONDS: 1e9,
        TimeUnit.MICROSECONDS: 1e6,
        TimeUnit.MILLISECONDS: 1e3,
        TimeUnit.SECONDS: 1,
    }
    return seconds * conversions[unit]


def log_performance(
    enabled: bool = False,
    unit: TimeUnit = TimeUnit.MILLISECONDS,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator that logs the execution time of functions when enabled.

    Args:
        enabled (bool): Flag to enable/disable performance logging
        unit (TimeUnit): Time unit for logging (default: milliseconds)

    Returns:
        Callable: The decorated function
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if not enabled:
                return func(*args, **kwargs)

            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()

            execution_time = _convert_time(end_time - start_time, unit)
            Printer.print_light_grey_message(
                f"⚡ Performance: {func.__name__} took {execution_time:.2f}{unit.value}"
            )

            return result

        return cast(Callable[P, R], wrapper)

    return decorator
