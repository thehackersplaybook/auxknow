from rich import print as rprint
from enum import Enum


class PrinterColor(Enum):
    DEFAULT = "bright_white"
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"
    BRIGHT_BLACK = "bright_black"
    BRIGHT_RED = "bright_red"
    BRIGHT_GREEN = "bright_green"
    BRIGHT_YELLOW = "bright_yellow"
    BRIGHT_BLUE = "bright_blue"
    BRIGHT_MAGENTA = "bright_magenta"
    BRIGHT_CYAN = "bright_cyan"
    BRIGHT_WHITE = "bright_white"
    GREY0 = "grey0"
    NAVY_BLUE = "navy_blue"
    DARK_BLUE = "dark_blue"
    BLUE3 = "blue3"
    BLUE1 = "blue1"
    DARK_GREEN = "dark_green"
    DEEP_SKY_BLUE4 = "deep_sky_blue4"
    DODGER_BLUE3 = "dodger_blue3"
    DODGER_BLUE2 = "dodger_blue2"
    GREEN4 = "green4"
    SPRING_GREEN4 = "spring_green4"
    TURQUOISE4 = "turquoise4"
    DEEP_SKY_BLUE3 = "deep_sky_blue3"
    DODGER_BLUE1 = "dodger_blue1"
    DARK_CYAN = "dark_cyan"
    LIGHT_SEA_GREEN = "light_sea_green"
    DEEP_SKY_BLUE2 = "deep_sky_blue2"
    DEEP_SKY_BLUE1 = "deep_sky_blue1"
    GREEN3 = "green3"
    SPRING_GREEN3 = "spring_green3"
    CYAN3 = "cyan3"
    DARK_TURQUOISE = "dark_turquoise"
    TURQUOISE2 = "turquoise2"
    GREEN1 = "green1"
    SPRING_GREEN2 = "spring_green2"
    SPRING_GREEN1 = "spring_green1"
    MEDIUM_SPRING_GREEN = "medium_spring_green"
    CYAN2 = "cyan2"
    CYAN1 = "cyan1"
    PURPLE4 = "purple4"
    PURPLE3 = "purple3"
    BLUE_VIOLET = "blue_violet"
    GREY37 = "grey37"
    MEDIUM_PURPLE4 = "medium_purple4"
    SLATE_BLUE3 = "slate_blue3"
    ROYAL_BLUE1 = "royal_blue1"
    CHARTREUSE4 = "chartreuse4"
    PALE_TURQUOISE4 = "pale_turquoise4"
    STEEL_BLUE = "steel_blue"
    STEEL_BLUE3 = "steel_blue3"
    CORNFLOWER_BLUE = "cornflower_blue"
    DARK_SEA_GREEN4 = "dark_sea_green4"
    CADET_BLUE = "cadet_blue"
    SKY_BLUE3 = "sky_blue3"
    CHARTREUSE3 = "chartreuse3"
    SEA_GREEN3 = "sea_green3"
    AQUAMARINE3 = "aquamarine3"
    MEDIUM_TURQUOISE = "medium_turquoise"
    STEEL_BLUE1 = "steel_blue1"
    SEA_GREEN2 = "sea_green2"
    SEA_GREEN1 = "sea_green1"
    DARK_SLATE_GRAY2 = "dark_slate_gray2"
    DARK_RED = "dark_red"
    DARK_MAGENTA = "dark_magenta"
    ORANGE4 = "orange4"
    LIGHT_PINK4 = "light_pink4"
    PLUM4 = "plum4"
    MEDIUM_PURPLE3 = "medium_purple3"
    SLATE_BLUE1 = "slate_blue1"
    WHEAT4 = "wheat4"
    GREY53 = "grey53"
    LIGHT_SLATE_GREY = "light_slate_grey"
    MEDIUM_PURPLE = "medium_purple"
    LIGHT_SLATE_BLUE = "light_slate_blue"
    YELLOW4 = "yellow4"
    DARK_SEA_GREEN = "dark_sea_green"
    LIGHT_SKY_BLUE3 = "light_sky_blue3"
    SKY_BLUE2 = "sky_blue2"
    CHARTREUSE2 = "chartreuse2"
    PALE_GREEN3 = "pale_green3"
    DARK_SLATE_GRAY3 = "dark_slate_gray3"
    SKY_BLUE1 = "sky_blue1"
    CHARTREUSE1 = "chartreuse1"
    LIGHT_GREEN = "light_green"
    AQUAMARINE1 = "aquamarine1"
    DARK_SLATE_GRAY1 = "dark_slate_gray1"
    DEEP_PINK4 = "deep_pink4"
    MEDIUM_VIOLET_RED = "medium_violet_red"
    DARK_VIOLET = "dark_violet"
    PURPLE = "purple"
    MEDIUM_ORCHID3 = "medium_orchid3"
    MEDIUM_ORCHID = "medium_orchid"
    DARK_GOLDENROD = "dark_goldenrod"
    ROSY_BROWN = "rosy_brown"
    GREY63 = "grey63"
    MEDIUM_PURPLE2 = "medium_purple2"
    MEDIUM_PURPLE1 = "medium_purple1"
    DARK_KHAKI = "dark_khaki"
    NAVAJO_WHITE3 = "navajo_white3"
    GREY69 = "grey69"
    LIGHT_STEEL_BLUE3 = "light_steel_blue3"
    LIGHT_STEEL_BLUE = "light_steel_blue"
    DARK_OLIVE_GREEN3 = "dark_olive_green3"
    DARK_SEA_GREEN3 = "dark_sea_green3"
    LIGHT_CYAN3 = "light_cyan3"
    LIGHT_SKY_BLUE1 = "light_sky_blue1"
    GREEN_YELLOW = "green_yellow"
    DARK_OLIVE_GREEN2 = "dark_olive_green2"
    PALE_GREEN1 = "pale_green1"
    DARK_SEA_GREEN2 = "dark_sea_green2"
    PALE_TURQUOISE1 = "pale_turquoise1"
    RED3 = "red3"
    DEEP_PINK3 = "deep_pink3"
    MAGENTA3 = "magenta3"
    DARK_ORANGE3 = "dark_orange3"
    INDIAN_RED = "indian_red"
    HOT_PINK3 = "hot_pink3"
    HOT_PINK2 = "hot_pink2"
    ORCHID = "orchid"
    ORANGE3 = "orange3"
    LIGHT_SALMON3 = "light_salmon3"
    LIGHT_PINK3 = "light_pink3"
    PINK3 = "pink3"
    PLUM3 = "plum3"
    VIOLET = "violet"
    GOLD3 = "gold3"
    LIGHT_GOLDENROD3 = "light_goldenrod3"
    TAN = "tan"
    MISTY_ROSE3 = "misty_rose3"
    THISTLE3 = "thistle3"
    PLUM2 = "plum2"
    YELLOW3 = "yellow3"
    KHAKI3 = "khaki3"
    LIGHT_YELLOW3 = "light_yellow3"
    GREY84 = "grey84"
    LIGHT_STEEL_BLUE1 = "light_steel_blue1"
    YELLOW2 = "yellow2"
    DARK_OLIVE_GREEN1 = "dark_olive_green1"
    DARK_SEA_GREEN1 = "dark_sea_green1"
    HONEYDEW2 = "honeydew2"
    LIGHT_CYAN1 = "light_cyan1"
    RED1 = "red1"
    DEEP_PINK2 = "deep_pink2"
    DEEP_PINK1 = "deep_pink1"
    MAGENTA2 = "magenta2"
    MAGENTA1 = "magenta1"
    ORANGE_RED1 = "orange_red1"
    INDIAN_RED1 = "indian_red1"
    HOT_PINK = "hot_pink"
    MEDIUM_ORCHID1 = "medium_orchid1"
    DARK_ORANGE = "dark_orange"
    SALMON1 = "salmon1"
    LIGHT_CORAL = "light_coral"
    PALE_VIOLET_RED1 = "pale_violet_red1"
    ORCHID2 = "orchid2"
    ORCHID1 = "orchid1"
    ORANGE1 = "orange1"
    SANDY_BROWN = "sandy_brown"
    LIGHT_SALMON1 = "light_salmon1"
    LIGHT_PINK1 = "light_pink1"
    PINK1 = "pink1"
    PLUM1 = "plum1"
    GOLD1 = "gold1"
    LIGHT_GOLDENROD2 = "light_goldenrod2"
    NAVAJO_WHITE1 = "navajo_white1"
    MISTY_ROSE1 = "misty_rose1"
    THISTLE1 = "thistle1"
    YELLOW1 = "yellow1"
    LIGHT_GOLDENROD1 = "light_goldenrod1"
    KHAKI1 = "khaki1"
    WHEAT1 = "wheat1"
    CORNSILK1 = "cornsilk1"
    GREY100 = "grey100"
    GREY3 = "grey3"
    GREY7 = "grey7"
    GREY11 = "grey11"
    GREY15 = "grey15"
    GREY19 = "grey19"
    GREY23 = "grey23"
    GREY27 = "grey27"
    GREY30 = "grey30"
    GREY35 = "grey35"
    GREY39 = "grey39"
    GREY42 = "grey42"
    GREY46 = "grey46"
    GREY50 = "grey50"
    GREY54 = "grey54"
    GREY58 = "grey58"
    GREY62 = "grey62"
    GREY66 = "grey66"
    GREY70 = "grey70"
    GREY74 = "grey74"
    GREY78 = "grey78"
    GREY82 = "grey82"
    GREY85 = "grey85"
    GREY89 = "grey89"
    GREY93 = "grey93"


class Printer:
    """Printer class for printing messages."""

    @staticmethod
    def print_message(message: str, color: PrinterColor = PrinterColor.DEFAULT):
        """Print a message with a color."""
        rprint(f"[{color.value}]{message}[/{color.value}]")

    @staticmethod
    def print_orange_message(message: str):
        """Print an orange message."""
        Printer.print_message(message, PrinterColor.DARK_ORANGE3)

    @staticmethod
    def print_blue_message(message: str):
        """Print a blue message."""
        Printer.print_message(message, PrinterColor.BLUE)

    @staticmethod
    def print_green_message(message: str):
        """Print a green message."""
        Printer.print_message(message, PrinterColor.GREEN)

    @staticmethod
    def print_red_message(message: str):
        """Print a red message."""
        Printer.print_message(message, PrinterColor.RED)

    @staticmethod
    def print_yellow_message(message: str):
        """Print a yellow message."""
        Printer.print_message(message, PrinterColor.YELLOW)

    @staticmethod
    def print_magenta_message(message: str):
        """Print a magenta message."""
        Printer.print_message(message, PrinterColor.MAGENTA)

    @staticmethod
    def print_cyan_message(message: str):
        """Print a cyan message."""
        Printer.print_message(message, PrinterColor.CYAN)

    @staticmethod
    def print_white_message(message: str):
        """Print a white message."""
        Printer.print_message(message, PrinterColor.WHITE)

    @staticmethod
    def print_bright_black_message(message: str):
        """Print a bright black message."""
        Printer.print_message(message, PrinterColor.BRIGHT_BLACK)

    @staticmethod
    def print_bright_red_message(message: str):
        """Print a bright red message."""
        Printer.print_message(message, PrinterColor.BRIGHT_RED)

    @staticmethod
    def print_bright_green_message(message: str):
        """Print a bright green message."""
        Printer.print_message(message, PrinterColor.BRIGHT_GREEN)

    @staticmethod
    def print_bright_yellow_message(message: str):
        """Print a bright yellow message."""
        Printer.print_message(message, PrinterColor.BRIGHT_YELLOW)

    @staticmethod
    def print_bright_blue_message(message: str):
        """Print a bright blue message."""
        Printer.print_message(message, PrinterColor.BRIGHT_BLUE)

    @staticmethod
    def print_bright_magenta_message(message: str):
        """Print a bright magenta message."""
        Printer.print_message(message, PrinterColor.BRIGHT_MAGENTA)

    @staticmethod
    def print_bright_cyan_message(message: str):
        """Print a bright cyan message."""
        Printer.print_message(message, PrinterColor.BRIGHT_CYAN)

    @staticmethod
    def print_bright_white_message(message: str):
        """Print a bright white message."""
        Printer.print_message(message, PrinterColor.BRIGHT_WHITE)

    @staticmethod
    def print_light_grey_message(message: str):
        """Print a light grey message."""
        Printer.print_message(message, PrinterColor.GREY0)

    @staticmethod
    def print_navy_blue_message(message: str):
        """Print a navy blue message."""
        Printer.print_message(message, PrinterColor.NAVY_BLUE)
