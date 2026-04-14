from dataclasses import dataclass, field, fields
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
        for f in fields(self):
            value = getattr(self, f.name)

            # Type validation based on dataclass field type
            if f.type == int:
                if not isinstance(value, int) or isinstance(value, bool):
                    raise TypeError(f"Field '{f.name}' must be of type int, got {type(value).__name__}")

            # Range validation: most status fields should be non-negative
            if f.name in ["hp", "max_hp", "power", "max_power", "level", "gold", "exp", "hunger"]:
                if value < 0:
                    raise ValueError(f"Field '{f.name}' must be non-negative, got {value}")

            # Specific logic: level must be at least 1
            if f.name == "level" and value == 0:
                raise ValueError("Field 'level' must be at least 1")
