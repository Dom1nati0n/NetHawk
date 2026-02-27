import numpy as np
from dataclasses import dataclass, field

# Tile Constants
WALL = 0
FLOOR = 1

@dataclass
class LevelMap:
    width: int
    height: int
    # 2D array of integers representing tile types
    tiles: np.ndarray = field(init=False)

    def __post_init__(self):
        # Initialize with WALLs
        self.tiles = np.full((self.height, self.width), WALL, dtype=np.int8)
