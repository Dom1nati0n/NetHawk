from dataclasses import dataclass
from enum import Enum, auto

class Alignment(Enum):
    LAWFUL = auto()
    NEUTRAL = auto()
    CHAOTIC = auto()

class Gender(Enum):
    MALE = auto()
    FEMALE = auto()
    NEUTER = auto() # For monsters

class Race(Enum):
    HUMAN = auto()
    ELF = auto()
    DWARF = auto()
    GNOME = auto()
    ORC = auto()

class Role(Enum):
    ARCHEOLOGIST = auto()
    BARBARIAN = auto()
    CAVEMAN = auto()
    HEALER = auto()
    KNIGHT = auto()
    MONK = auto()
    PRIEST = auto()
    RANGER = auto()
    ROGUE = auto()
    SAMURAI = auto()
    TOURIST = auto()
    VALKYRIE = auto()
    WIZARD = auto()

@dataclass
class Identity:
    name: str
    role: Role
    race: Race
    gender: Gender
    alignment: Alignment
