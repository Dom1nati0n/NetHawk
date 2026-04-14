import unittest
import sys
from unittest.mock import MagicMock

# Mock numpy to allow importing components without actual dependency
sys.modules["numpy"] = MagicMock()

from src.nethawk.components.attributes import Attributes

class TestAttributes(unittest.TestCase):
    def test_valid_attributes(self):
        # Should instantiate successfully
        attr = Attributes(
            strength=10,
            dexterity=12,
            constitution=14,
            intelligence=16,
            wisdom=8,
            charisma=10
        )
        self.assertEqual(attr.strength, 10)
        self.assertEqual(attr.max_strength, 18)

    def test_invalid_types_raise_type_error(self):
        # String instead of int
        with self.assertRaisesRegex(TypeError, "'strength' must be an integer"):
            Attributes(
                strength="10",
                dexterity=12,
                constitution=14,
                intelligence=16,
                wisdom=8,
                charisma=10
            )

        # Float instead of int
        with self.assertRaisesRegex(TypeError, "'dexterity' must be an integer"):
            Attributes(
                strength=10,
                dexterity=12.5,
                constitution=14,
                intelligence=16,
                wisdom=8,
                charisma=10
            )

        # Boolean instead of int
        with self.assertRaisesRegex(TypeError, "'constitution' must be an integer"):
            Attributes(
                strength=10,
                dexterity=12,
                constitution=True,
                intelligence=16,
                wisdom=8,
                charisma=10
            )

        # Invalid max attribute type
        with self.assertRaisesRegex(TypeError, "'max_intelligence' must be an integer"):
            Attributes(
                strength=10,
                dexterity=12,
                constitution=14,
                intelligence=16,
                wisdom=8,
                charisma=10,
                max_intelligence="20"
            )

    def test_out_of_bounds_raise_value_error(self):
        # Negative value
        with self.assertRaisesRegex(ValueError, "'wisdom' must be between 0 and 18"):
            Attributes(
                strength=10,
                dexterity=12,
                constitution=14,
                intelligence=16,
                wisdom=-5,
                charisma=10
            )

        # Above max default
        with self.assertRaisesRegex(ValueError, "'charisma' must be between 0 and 18"):
            Attributes(
                strength=10,
                dexterity=12,
                constitution=14,
                intelligence=16,
                wisdom=8,
                charisma=20
            )

        # Above custom max
        with self.assertRaisesRegex(ValueError, "'strength' must be between 0 and 10"):
            Attributes(
                strength=12,
                dexterity=12,
                constitution=14,
                intelligence=16,
                wisdom=8,
                charisma=10,
                max_strength=10
            )

if __name__ == '__main__':
    unittest.main()
