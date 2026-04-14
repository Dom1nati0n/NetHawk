from dataclasses import dataclass, field
from typing import List
from ..engine.ecs import Entity

@dataclass
class Item:
    name: str
    weight: float = 0.0

@dataclass
class Inventory:
    items: List[Entity] = field(default_factory=list)
    capacity: float = 100.0
