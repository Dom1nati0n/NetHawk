import unittest
from unittest.mock import MagicMock
import sys

# Mock numpy before importing modules that depend on it
mock_np = MagicMock()
mock_np.float32 = float
# NetHawk components use index-based assignment, so we need a mutable sequence
mock_np.zeros.side_effect = lambda shape, dtype=None: [0.0] * (shape if isinstance(shape, int) else shape[0])
mock_np.array.side_effect = lambda data, dtype=None: data
sys.modules["numpy"] = mock_np

from src.nethawk.engine.ecs import World
from src.nethawk.main import create_player
from src.nethawk.components import Identity, Attributes, Status, Position, Velocity, Alignment, Gender

class TestPlayerCreation(unittest.TestCase):
    def setUp(self):
        self.world = World()

    def test_create_player_components(self):
        player = create_player(self.world)

        # Verify entity exists
        self.assertIsNotNone(player)

        # Identity
        identity = self.world.get_component(player, Identity)
        self.assertIsNotNone(identity)
        self.assertEqual(identity.name, "Player")
        self.assertEqual(identity.role, "Tourist")
        self.assertEqual(identity.race, "Human")
        self.assertEqual(identity.gender, Gender.FEMALE)
        self.assertEqual(identity.alignment, Alignment.NEUTRAL)

        # Attributes
        attrs = self.world.get_component(player, Attributes)
        self.assertIsNotNone(attrs)
        self.assertEqual(attrs.strength, 12)
        self.assertEqual(attrs.dexterity, 7)
        self.assertEqual(attrs.constitution, 18)
        self.assertEqual(attrs.intelligence, 11)
        self.assertEqual(attrs.wisdom, 9)
        self.assertEqual(attrs.charisma, 15)

        # Status
        status = self.world.get_component(player, Status)
        self.assertIsNotNone(status)
        self.assertEqual(status.hp, 9)
        self.assertEqual(status.max_hp, 12)
        self.assertEqual(status.power, 3)
        self.assertEqual(status.max_power, 3)
        self.assertEqual(status.ac, 10)
        self.assertEqual(status.level, 1)
        self.assertEqual(status.gold, 993)
        self.assertEqual(status.exp, 19)
        self.assertEqual(status.hunger, 1)

        # Position
        pos = self.world.get_component(player, Position)
        self.assertIsNotNone(pos)
        self.assertEqual(pos.x, 10.0)
        self.assertEqual(pos.y, 10.0)

        # Velocity
        vel = self.world.get_component(player, Velocity)
        self.assertIsNotNone(vel)
        self.assertEqual(vel.vector, [1.0, 0.0])

if __name__ == '__main__':
    unittest.main()
