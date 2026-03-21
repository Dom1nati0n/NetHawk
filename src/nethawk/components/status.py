from dataclasses import dataclass, field
from typing import Set

@dataclass
class Status:
    hp: int
    max_hp: int
    power: int
    max_power: int
    ac: int
    level: int
    gold: int
    exp: int
    hunger: int
    conditions: Set[str] = field(default_factory=set) # e.g. "blind", "confused"

    def __post_init__(self):
        if self.max_hp < 1:
            raise ValueError(f"max_hp must be >= 1, got {self.max_hp}")
        if self.max_power < 0:
            raise ValueError(f"max_power must be >= 0, got {self.max_power}")
        if self.level < 1:
            raise ValueError(f"level must be >= 1, got {self.level}")
        if self.gold < 0:
            raise ValueError(f"gold cannot be negative, got {self.gold}")
        if self.exp < 0:
            raise ValueError(f"exp cannot be negative, got {self.exp}")
