import unittest
import sys
from unittest.mock import MagicMock

# Mock numpy before imports
sys.modules['numpy'] = MagicMock()

from nethawk.engine.ecs import World, ComponentManager, EntityManager

class DummyComponent1:
    pass

class DummyComponent2:
    pass

class TestECSVerify(unittest.TestCase):
    def test_destroy_entity(self):
        world = World()
        entity = world.create_entity()
        comp1 = DummyComponent1()
        comp2 = DummyComponent2()

        world.add_component(entity, comp1)
        world.add_component(entity, comp2)

        self.assertTrue(world.has_component(entity, DummyComponent1))
        self.assertTrue(world.has_component(entity, DummyComponent2))

        world.destroy_entity(entity)

        self.assertFalse(world.has_component(entity, DummyComponent1))
        self.assertFalse(world.has_component(entity, DummyComponent2))

if __name__ == '__main__':
    unittest.main()
