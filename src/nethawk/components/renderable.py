from dataclasses import dataclass
from enum import Enum, auto

class Color(Enum):
    BLACK = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    MAGENTA = auto()
    CYAN = auto()
    WHITE = auto()

@dataclass
class Renderable:
    glyph: str
    color: Color
