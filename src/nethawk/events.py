from dataclasses import dataclass
from .engine.ecs import Entity

@dataclass
class PickupEvent:
    actor: Entity
    item: Entity

@dataclass
class DropEvent:
    actor: Entity
    item: Entity
