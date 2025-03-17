import pytest
from unittest.mock import patch, call
from auxknow.common.printer import Printer, PrinterColor


@pytest.fixture
def mock_rprint():
    with patch("auxknow.common.printer.rprint") as mock:
        yield mock


def test_verbose_logger_with_valid_message(mock_rprint):
    test_message = "test message"
    Printer.verbose_logger(True, mock_rprint, test_message)
    mock_rprint.assert_called_once_with(test_message)


def test_verbose_logger_when_not_verbose(mock_rprint):
    Printer.verbose_logger(False, mock_rprint, "test message")
    mock_rprint.assert_not_called()


def test_verbose_logger_with_empty_message(mock_rprint):
    Printer.verbose_logger(True, mock_rprint, "")
    mock_rprint.assert_not_called()


def test_verbose_logger_with_whitespace_message(mock_rprint):
    Printer.verbose_logger(True, mock_rprint, "   ")
    mock_rprint.assert_not_called()


def test_print_message_default_color(mock_rprint):
    message = "test message"
    Printer.print_message(message)
    mock_rprint.assert_called_once_with(
        f"[{PrinterColor.DEFAULT.value}]{message}[/{PrinterColor.DEFAULT.value}]"
    )


@pytest.mark.parametrize(
    "color_method,color_enum",
    [
        (Printer.print_orange_message, PrinterColor.DARK_ORANGE3),
        (Printer.print_blue_message, PrinterColor.BLUE),
        (Printer.print_green_message, PrinterColor.GREEN),
        (Printer.print_red_message, PrinterColor.RED),
        (Printer.print_yellow_message, PrinterColor.YELLOW),
        (Printer.print_magenta_message, PrinterColor.MAGENTA),
        (Printer.print_cyan_message, PrinterColor.CYAN),
        (Printer.print_white_message, PrinterColor.WHITE),
        (Printer.print_bright_black_message, PrinterColor.BRIGHT_BLACK),
        (Printer.print_bright_red_message, PrinterColor.BRIGHT_RED),
        (Printer.print_bright_green_message, PrinterColor.BRIGHT_GREEN),
        (Printer.print_bright_yellow_message, PrinterColor.BRIGHT_YELLOW),
        (Printer.print_bright_blue_message, PrinterColor.BRIGHT_BLUE),
        (Printer.print_bright_magenta_message, PrinterColor.BRIGHT_MAGENTA),
        (Printer.print_bright_cyan_message, PrinterColor.BRIGHT_CYAN),
        (Printer.print_bright_white_message, PrinterColor.BRIGHT_WHITE),
        (Printer.print_light_grey_message, PrinterColor.GREY0),
        (Printer.print_navy_blue_message, PrinterColor.NAVY_BLUE),
    ],
)
def test_color_print_methods(mock_rprint, color_method, color_enum):
    message = "test message"
    color_method(message)
    mock_rprint.assert_called_once_with(
        f"[{color_enum.value}]{message}[/{color_enum.value}]"
    )


def test_print_message_with_special_characters(mock_rprint):
    message = "test\nmessage\twith\rspecial\u0020chars"
    Printer.print_message(message)
    mock_rprint.assert_called_once_with(
        f"[{PrinterColor.DEFAULT.value}]{message}[/{PrinterColor.DEFAULT.value}]"
    )


def test_multiple_print_calls(mock_rprint):
    messages = ["first", "second", "third"]
    for msg in messages:
        Printer.print_message(msg)

    expected_calls = [
        call(f"[{PrinterColor.DEFAULT.value}]{msg}[/{PrinterColor.DEFAULT.value}]")
        for msg in messages
    ]
    assert mock_rprint.call_args_list == expected_calls


def test_print_message_empty_string(mock_rprint):
    Printer.print_message("")
    mock_rprint.assert_called_once_with(
        f"[{PrinterColor.DEFAULT.value}][/{PrinterColor.DEFAULT.value}]"
    )


def test_print_message_none(mock_rprint):
    """Test that print_message raises TypeError when message is None."""
    with pytest.raises(TypeError, match="Message must be a string"):
        Printer.print_message(None)


def test_print_message_invalid_types(mock_rprint):
    """Test that print_message raises TypeError for non-string types."""
    invalid_inputs = [123, 45.67, [], {}, set(), True]
    for invalid_input in invalid_inputs:
        with pytest.raises(TypeError, match="Message must be a string"):
            Printer.print_message(invalid_input)
