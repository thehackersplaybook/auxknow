import time
import functools
from .printer import Printer
from .models import TimeUnit
from .constants import Constants


def _convert_time(seconds: float, unit: TimeUnit) -> float:
    """Convert time from seconds to specified unit

    Args:
        seconds (float): Time in seconds
        unit (TimeUnit): The unit to convert to

    Returns:
        float: Time in specified unit
    """
    conversions = {
        TimeUnit.NANOSECONDS: 1e9,
        TimeUnit.MICROSECONDS: 1e6,
        TimeUnit.MILLISECONDS: 1e3,
        TimeUnit.SECONDS: 1,
    }
    return seconds * conversions[unit]


def log_performance(enabled=lambda self: False, unit: TimeUnit = TimeUnit.MILLISECONDS):
    """Decorator to log performance of functions.

    Args:
        enabled (callable): A function that takes self and returns bool indicating if logging is enabled
        unit (TimeUnit): The unit to display the time in (default: milliseconds)
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not enabled(self) or not self.config.performance_logging_enabled:
                return func(self, *args, **kwargs)

            start_time = time.time()
            result = func(self, *args, **kwargs)

            if self.config.performance_logging_enabled:
                end_time = time.time()
                duration = _convert_time(end_time - start_time, unit)
                Printer.print_yellow_message(
                    Constants.PERFORMANCE_LOG_MESSAGE(
                        func.__name__, duration, unit.value
                    )
                )

            return result

        return wrapper

    return decorator
