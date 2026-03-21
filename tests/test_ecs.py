import unittest
from src.nethawk.engine.ecs import World, Entity

class MockComponentA:
    pass

class MockComponentB:
    pass

class TestECS(unittest.TestCase):
    def setUp(self):
        self.world = World()

    def test_entity_creation(self):
        entity = self.world.create_entity()
        self.assertIsInstance(entity, int)

    def test_add_get_has_component(self):
        entity = self.world.create_entity()
        comp_a = MockComponentA()

        self.world.add_component(entity, comp_a)

        self.assertTrue(self.world.has_component(entity, MockComponentA))
        self.assertEqual(self.world.get_component(entity, MockComponentA), comp_a)
        self.assertFalse(self.world.has_component(entity, MockComponentB))

    def test_remove_component(self):
        entity = self.world.create_entity()
        comp_a = MockComponentA()
        self.world.add_component(entity, comp_a)

        self.world.remove_component(entity, MockComponentA)
        self.assertFalse(self.world.has_component(entity, MockComponentA))

    def test_destroy_entity_removes_components(self):
        entity = self.world.create_entity()
        comp_a = MockComponentA()
        comp_b = MockComponentB()

        self.world.add_component(entity, comp_a)
        self.world.add_component(entity, comp_b)

        self.assertTrue(self.world.has_component(entity, MockComponentA))
        self.assertTrue(self.world.has_component(entity, MockComponentB))

        self.world.destroy_entity(entity)

        # After destruction, components should be gone from the manager
        self.assertFalse(self.world.has_component(entity, MockComponentA))
        self.assertFalse(self.world.has_component(entity, MockComponentB))

if __name__ == '__main__':
    unittest.main()
