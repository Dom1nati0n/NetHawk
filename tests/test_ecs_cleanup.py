import unittest
from dataclasses import dataclass
from src.nethawk.engine.ecs import World

@dataclass
class MockComponentA:
    value: int = 0

@dataclass
class MockComponentB:
    name: str = "test"

class TestECSCleanup(unittest.TestCase):
    def setUp(self):
        self.world = World()

    def test_entity_destruction_removes_components(self):
        # 1. Create an entity and add components
        entity = self.world.create_entity()
        comp_a = MockComponentA(value=42)
        comp_b = MockComponentB(name="cleanup_test")

        self.world.add_component(entity, comp_a)
        self.world.add_component(entity, comp_b)

        # 2. Verify components are present
        self.assertTrue(self.world.has_component(entity, MockComponentA))
        self.assertTrue(self.world.has_component(entity, MockComponentB))
        self.assertEqual(self.world.get_component(entity, MockComponentA).value, 42)

        # 3. Destroy the entity
        self.world.destroy_entity(entity)

        # 4. Verify components are removed from ComponentManager
        # We check via the World's interface
        self.assertFalse(self.world.has_component(entity, MockComponentA))
        self.assertIsNone(self.world.get_component(entity, MockComponentA))
        self.assertFalse(self.world.has_component(entity, MockComponentB))

        # Also check internal ComponentManager state to be sure
        self.assertNotIn(entity, self.world.component_manager.get_components(MockComponentA))
        self.assertNotIn(entity, self.world.component_manager.get_components(MockComponentB))

if __name__ == '__main__':
    unittest.main()
