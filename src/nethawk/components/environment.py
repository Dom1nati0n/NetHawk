from enum import Enum, auto

class TileType(Enum):
    VOID = auto()
    FLOOR = auto()
    WALL = auto()
    DOOR = auto()
    STAIRS_UP = auto()
    STAIRS_DOWN = auto()
