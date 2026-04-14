import unittest
from src.nethawk.engine.ecs import World

class MockComponentA:
    pass

class MockComponentB:
    pass

class TestECSCleanup(unittest.TestCase):
    def setUp(self):
        self.world = World()

    def test_destroy_entity_removes_components(self):
        # 1. Create an entity and add components
        entity = self.world.create_entity()
        comp_a = MockComponentA()
        comp_b = MockComponentB()

        self.world.add_component(entity, comp_a)
        self.world.add_component(entity, comp_b)

        # Verify components are added
        self.assertTrue(self.world.has_component(entity, MockComponentA))
        self.assertTrue(self.world.has_component(entity, MockComponentB))

        # 2. Destroy the entity
        self.world.destroy_entity(entity)

        # 3. Verify components are removed from ComponentManager
        self.assertFalse(self.world.has_component(entity, MockComponentA))
        self.assertFalse(self.world.has_component(entity, MockComponentB))

        # Check internal storage for thoroughness
        for comp_type in [MockComponentA, MockComponentB]:
            self.assertNotIn(entity, self.world.component_manager.get_components(comp_type))

if __name__ == '__main__':
    unittest.main()
