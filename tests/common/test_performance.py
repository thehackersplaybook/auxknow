import unittest
from unittest.mock import patch, Mock
from auxknow.common.performance import _convert_time, log_performance
from auxknow.common.models import TimeUnit
from auxknow.common.constants import Constants


class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.mock_config = Mock()
        self.mock_config.performance_logging_enabled = True

    def test_convert_time(self):
        # Test all time unit conversions
        self.assertEqual(_convert_time(1, TimeUnit.SECONDS), 1)
        self.assertEqual(_convert_time(1, TimeUnit.MILLISECONDS), 1000)
        self.assertEqual(_convert_time(1, TimeUnit.MICROSECONDS), 1000000)
        self.assertEqual(_convert_time(1, TimeUnit.NANOSECONDS), 1000000000)

        # Test with decimal values
        self.assertEqual(_convert_time(0.5, TimeUnit.SECONDS), 0.5)
        self.assertEqual(_convert_time(0.1, TimeUnit.MILLISECONDS), 100)

    @patch("time.time")
    @patch("auxknow.common.printer.Printer.print_yellow_message")
    def test_log_performance_decorator_enabled(self, mock_print, mock_time):
        # Mock time.time() to return sequential values
        mock_time.side_effect = [100, 101]  # 1 second difference

        # Test class with decorated method
        class TestClass:
            def __init__(self):
                self.config = self.Config()

            class Config:
                performance_logging_enabled = True

            @log_performance(enabled=lambda self: True)
            def test_method(self):
                return "test"

        instance = TestClass()
        result = instance.test_method()

        self.assertEqual(result, "test")
        mock_print.assert_called_once_with(
            Constants.PERFORMANCE_LOG_MESSAGE("test_method", 1000, "ms")
        )

    @patch("time.time")
    @patch("auxknow.common.printer.Printer.print_yellow_message")
    def test_log_performance_decorator_disabled(self, mock_print, mock_time):
        class TestClass:
            def __init__(self):
                self.config = self.Config()

            class Config:
                performance_logging_enabled = False

            @log_performance(enabled=lambda self: False)
            def test_method(self):
                return "test"

        instance = TestClass()
        result = instance.test_method()

        self.assertEqual(result, "test")
        mock_print.assert_not_called()

    @patch("time.time")
    @patch("auxknow.common.printer.Printer.print_yellow_message")
    def test_log_performance_with_different_time_units(self, mock_print, mock_time):
        mock_time.side_effect = [100, 101]  # 1 second difference

        class TestClass:
            def __init__(self):
                self.config = self.Config()

            class Config:
                performance_logging_enabled = True

            @log_performance(enabled=lambda self: True, unit=TimeUnit.MICROSECONDS)
            def test_method(self):
                return "test"

        instance = TestClass()
        result = instance.test_method()

        self.assertEqual(result, "test")
        # Note: Using micro symbol 'µ' (U+00B5) instead of 'μ' (U+03BC)
        mock_print.assert_called_once_with(
            Constants.PERFORMANCE_LOG_MESSAGE("test_method", 1000000, "µs")
        )

    def test_log_performance_with_args_kwargs(self):
        class TestClass:
            def __init__(self):
                self.config = self.Config()

            class Config:
                performance_logging_enabled = True

            @log_performance(enabled=lambda self: True)
            def test_method(self, arg1, kwarg1=None):
                return f"{arg1}-{kwarg1}"

        instance = TestClass()
        result = instance.test_method("test", kwarg1="value")
        self.assertEqual(result, "test-value")


if __name__ == "__main__":
    unittest.main()
