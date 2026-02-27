from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

class ItemType(Enum):
    WEAPON = auto()
    ARMOR = auto()
    POTION = auto()
    SCROLL = auto()
    WAND = auto()
    RING = auto()
    AMULET = auto()
    TOOL = auto()
    FOOD = auto()
    GEM = auto()
    GOLD = auto()

@dataclass
class Item:
    type: ItemType
    weight: float = 0.0
    count: int = 1
    identified: bool = False
    blessed: Optional[bool] = None # None means uncursed, True blessed, False cursed

@dataclass
class Weapon:
    # Damage expressed as dice notation e.g., "1d6" or tuples (num_dice, die_size)
    damage_small: tuple = (1, 6)
    damage_large: tuple = (1, 6)
    hit_bonus: int = 0
    damage_bonus: int = 0

@dataclass
class Armor:
    ac: int = 0
    type: str = "suit" # suit, shield, helm, gloves, boots, cloak, shirt
