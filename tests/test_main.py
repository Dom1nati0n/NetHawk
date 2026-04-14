import sys
import unittest
from unittest.mock import MagicMock, patch

# Locally mock numpy to prevent it from leaking to other tests in the suite
# Since main.py imports numpy at the top level, we must mock it before importing main.py.
# However, to avoid global state contamination, we restore sys.modules after import.
_original_numpy = sys.modules.get('numpy')
sys.modules['numpy'] = MagicMock()

from src.nethawk.main import create_player
from src.nethawk.engine.ecs import World
from src.nethawk.components import Identity, Attributes, Status, Position, Velocity, Alignment, Gender

# Restore numpy to its original state so other tests fail naturally with ModuleNotFoundError
# if numpy is not installed, instead of failing on mock assertions.
if _original_numpy is None:
    del sys.modules['numpy']
else:
    sys.modules['numpy'] = _original_numpy

class TestMain(unittest.TestCase):
    def test_create_player(self):
        world = World()
        player = create_player(world)

        # Verify Identity
        self.assertTrue(world.has_component(player, Identity))
        identity = world.get_component(player, Identity)
        self.assertEqual(identity.name, "Player")
        self.assertEqual(identity.role, "Valkyrie")
        self.assertEqual(identity.race, "Human")
        self.assertEqual(identity.gender, Gender.FEMALE)
        self.assertEqual(identity.alignment, Alignment.NEUTRAL)

        # Verify Attributes
        self.assertTrue(world.has_component(player, Attributes))
        attrs = world.get_component(player, Attributes)
        self.assertEqual(attrs.strength, 12)
        self.assertEqual(attrs.dexterity, 7)
        self.assertEqual(attrs.constitution, 18)
        self.assertEqual(attrs.intelligence, 11)
        self.assertEqual(attrs.wisdom, 9)
        self.assertEqual(attrs.charisma, 15)

        # Verify Status
        self.assertTrue(world.has_component(player, Status))
        status = world.get_component(player, Status)
        self.assertEqual(status.hp, 9)
        self.assertEqual(status.max_hp, 12)
        self.assertEqual(status.power, 3)
        self.assertEqual(status.max_power, 3)
        self.assertEqual(status.ac, 10)
        self.assertEqual(status.level, 1)
        self.assertEqual(status.gold, 993)
        self.assertEqual(status.exp, 19)
        self.assertEqual(status.hunger, 1)

        # Verify Position
        self.assertTrue(world.has_component(player, Position))
        # Since we deleted numpy from sys.modules, further instantiations that might dynamically
        # depend on numpy could fail. However, we already imported the modules needed and they
        # closed over the MagicMock. The Position component properties can still be accessed,
        # but the test logic itself is primarily focused on component existence and basic data.

        # Verify Velocity
        self.assertTrue(world.has_component(player, Velocity))

if __name__ == '__main__':
    unittest.main()
