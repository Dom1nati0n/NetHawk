import numpy as np
from dataclasses import dataclass, field

@dataclass
class Position:
    # Stored as a numpy array [x, y] using float32 for sub-pixel precision
    # This ensures smooth movement and frame independence
    coords: np.ndarray = field(default_factory=lambda: np.zeros(2, dtype=np.float32))
    
    @property
    def x(self) -> float:
        return self.coords[0]

    @property
    def y(self) -> float:
        return self.coords[1]
    
    @property
    def grid_x(self) -> int:
        return int(self.coords[0])

    @property
    def grid_y(self) -> int:
        return int(self.coords[1])

    def set(self, x: float, y: float) -> None:
        self.coords[0] = x
        self.coords[1] = y

@dataclass
class Velocity:
    # Stored as [vx, vy] in units per second
    vector: np.ndarray = field(default_factory=lambda: np.zeros(2, dtype=np.float32))
