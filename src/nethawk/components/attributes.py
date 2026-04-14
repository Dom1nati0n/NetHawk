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

    def __post_init__(self):
        attributes = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
        for attr in attributes:
            val = getattr(self, attr)
            max_val = getattr(self, f"max_{attr}")

            if not isinstance(val, int) or isinstance(val, bool):
                raise TypeError(f"'{attr}' must be an integer")
            if not isinstance(max_val, int) or isinstance(max_val, bool):
                raise TypeError(f"'max_{attr}' must be an integer")

            if val < 0 or val > max_val:
                raise ValueError(f"'{attr}' must be between 0 and {max_val}")
