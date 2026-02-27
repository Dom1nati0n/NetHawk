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
