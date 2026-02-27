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

@dataclass
class Identity:
    name: str
    role: str
    race: str
    gender: Gender
    alignment: Alignment
