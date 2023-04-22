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

    def __int__(self):
        return self.value

def reset():
    return '\033[0m'

def bold():
    return '\033[1m'

def underline():
    return '\033[4m'

def inverse():
    return '\033[7m'

def color(fg: Colors|int, bg: Colors|int|None=None):
    return f'\033[{30 + (int)(fg) + ((int)(fg) & 8)//2 * 13}' + (
        f';{40 + (int)(bg) + ((int)(bg) & 8)//2 * 13}' if bg else '') + 'm'


