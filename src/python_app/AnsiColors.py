from enum import Enum


class Colors(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    GRAY = 8
    BRIGHT_RED = 9
    BRIGHT_GREEN = 10
    BRIGHT_YELLOW = 11
    BRIGHT_BLUE = 12
    BRIGHT_MAGENTA = 13
    BRIGHT_CYAN = 14
    BRIGHT_WHITE = 15
    DEFAULT = 16

    def __int__(self):
        if self.value == 16:
            return 39
        elif self.value < 8:
            return self.value + 30
        else:
            return self.value + 82

    def __str__(self) -> str:
        return f'\033[{int(self)}m'


class Formatting(Enum):
    RESET = 0
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    RAPID_BLINK = 6
    INVERSE = 7
    CONCEAL = 8
    STRIKETHROUGH = 9
    FRAKTUR = 20  # hardly ever supported
    DOUBLE_UNDERLINE = 21
    LIGHT = 22  # neither BOLD or FAINT
    NONITALIC = 23
    REMOVE_UNDERLINE = 24
    FRAMED = 51
    ENCIRCLED = 52
    OVERLINED = 53
    UNFRAMED = 54
    REMOVE_OVERLINE = 55

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return f'\033[{self.value}m'


def reset():
    return '\033[0m'


def color(fg: Colors | int, bg: Colors | int | None = None) -> str:
    return f'\033[{int(fg)}' + (
        f';{int(bg) + 10}' if bg else '') + 'm'


class FormattedPrint(object):
    def __init__(self, fg: int | Colors | None = None,
                 bg: int | Colors | None = None) -> None:
        self.fg = fg
        self.bg = bg

    def __enter__(self):
        print(color(self.fg, self.bg), end=None)

    def __exit__(self, *args):
        print(reset(), end=None)
