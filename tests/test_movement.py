import unittest
import sys
from unittest.mock import MagicMock

# Mock numpy
class MockArray(list):
    def __add__(self, other):
        return MockArray([x + y for x, y in zip(self, other)])
    def __iadd__(self, other):
        for i in range(len(self)):
            self[i] += other[i]
        return self
    def __mul__(self, other):
        return MockArray([x * other for x in self])
    def __rmul__(self, other):
        return self.__mul__(other)

mock_np = MagicMock()
def mock_zeros(shape, dtype=None):
    if isinstance(shape, int):
        return MockArray([0.0] * shape)
    else:
        return MockArray([0.0] * shape[0])

mock_np.zeros.side_effect = mock_zeros
mock_np.float32 = float
sys.modules["numpy"] = mock_np

from src.nethawk.engine.ecs import World
from src.nethawk.components.spatial import Position, Velocity
from src.nethawk.systems.movement import movement_system

class TestMovementSystem(unittest.TestCase):
    def test_movement_update(self):
        world = World()
        entity = world.create_entity()

        pos = Position()
        pos.coords = MockArray([10.0, 20.0])
        world.add_component(entity, pos)

        vel = Velocity()
        vel.vector = MockArray([1.0, -2.0])
        world.add_component(entity, vel)

        # Update for 1.0 second
        movement_system(world, 1.0)

        self.assertEqual(pos.coords[0], 11.0)
        self.assertEqual(pos.coords[1], 18.0)

    def test_partial_components(self):
        world = World()

        # Entity with only Position
        e1 = world.create_entity()
        pos1 = Position()
        pos1.coords = MockArray([10.0, 10.0])
        world.add_component(e1, pos1)

        # Entity with only Velocity
        e2 = world.create_entity()
        vel2 = Velocity()
        vel2.vector = MockArray([1.0, 1.0])
        world.add_component(e2, vel2)

        movement_system(world, 1.0)

        # Position should not have changed
        self.assertEqual(pos1.coords[0], 10.0)
        self.assertEqual(pos1.coords[1], 10.0)

if __name__ == "__main__":
    unittest.main()
