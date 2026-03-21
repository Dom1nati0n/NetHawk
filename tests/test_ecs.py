import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from nethawk.engine.ecs import ComponentManager, World

class MockPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockVelocity:
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy

class TestECS(unittest.TestCase):
    def test_component_manager_basic(self):
        cm = ComponentManager()
        entity = 1
        pos = MockPosition(10, 20)

        # Test add and has
        cm.add_component(entity, pos)
        self.assertTrue(cm.has_component(entity, MockPosition))
        self.assertFalse(cm.has_component(entity, MockVelocity))
        self.assertFalse(cm.has_component(2, MockPosition))

        # Test get_component
        self.assertEqual(cm.get_component(entity, MockPosition), pos)
        self.assertIsNone(cm.get_component(entity, MockVelocity))
        self.assertIsNone(cm.get_component(2, MockPosition))

        # Test get_components
        positions = cm.get_components(MockPosition)
        self.assertEqual(len(positions), 1)
        self.assertEqual(positions[entity], pos)

        velocities = cm.get_components(MockVelocity)
        self.assertEqual(velocities, {})

    def test_world_integration(self):
        world = World()
        entity = world.create_entity()
        pos = MockPosition(10, 20)

        world.add_component(entity, pos)
        self.assertTrue(world.has_component(entity, MockPosition))
        self.assertEqual(world.get_component(entity, MockPosition), pos)

        world.destroy_entity(entity)
        self.assertFalse(world.has_component(entity, MockPosition))

if __name__ == "__main__":
    unittest.main()
