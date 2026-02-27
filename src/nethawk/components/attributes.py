from dataclasses import dataclass

@dataclass
class Attributes:
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    
    # Optional max values if attributes can be drained
    max_strength: int = 18
    max_dexterity: int = 18
    max_constitution: int = 18
    max_intelligence: int = 18
    max_wisdom: int = 18
    max_charisma: int = 18
