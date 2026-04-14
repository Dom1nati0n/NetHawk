import unittest
from nethawk.engine.ecs import ComponentManager

class MockComponent:
    pass

class AnotherComponent:
    pass

class TestComponentManager(unittest.TestCase):
    def setUp(self):
        self.manager = ComponentManager()
        self.entity = 1

    def test_remove_component_happy_path(self):
        """Test removing a component that the entity possesses."""
        comp = MockComponent()
        self.manager.add_component(self.entity, comp)
        self.assertTrue(self.manager.has_component(self.entity, MockComponent))

        self.manager.remove_component(self.entity, MockComponent)
        self.assertFalse(self.manager.has_component(self.entity, MockComponent))

    def test_remove_component_non_existent_type(self):
        """Test removing a component type that has never been registered."""
        # Should not raise any exception (e.g., KeyError)
        self.manager.remove_component(self.entity, MockComponent)

    def test_remove_component_non_existent_entity(self):
        """Test removing a component from an entity that doesn't have it, when the type exists."""
        # Add component to another entity so the type is registered
        comp = MockComponent()
        self.manager.add_component(2, comp)

        # Attempt to remove from self.entity (which doesn't have it)
        # Should not raise any exception
        self.manager.remove_component(self.entity, MockComponent)

if __name__ == "__main__":
    unittest.main()
