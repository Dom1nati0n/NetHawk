import unittest
from nethawk.engine.ecs import World

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Velocity:
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

class TestECS(unittest.TestCase):
    def test_entity_creation(self):
        world = World()
        e1 = world.create_entity()
        e2 = world.create_entity()
        self.assertNotEqual(e1, e2)

    def test_component_addition_retrieval(self):
        world = World()
        e = world.create_entity()
        pos = Position(10, 20)
        world.add_component(e, pos)

        retrieved_pos = world.get_component(e, Position)
        self.assertEqual(retrieved_pos.x, 10)
        self.assertEqual(retrieved_pos.y, 20)

    def test_has_component(self):
        world = World()
        e = world.create_entity()
        world.add_component(e, Position(0, 0))
        self.assertTrue(world.has_component(e, Position))
        self.assertFalse(world.has_component(e, Velocity))

    def test_entity_destruction_cleanup(self):
        world = World()
        e = world.create_entity()
        world.add_component(e, Position(1, 1))

        world.destroy_entity(e)
        self.assertIsNone(world.get_component(e, Position))

    def test_get_components_bulk(self):
        world = World()
        e1 = world.create_entity()
        e2 = world.create_entity()
        world.add_component(e1, Position(1, 1))
        world.add_component(e2, Position(2, 2))

        positions = world.get_components(Position)
        self.assertEqual(len(positions), 2)
        self.assertIn(e1, positions)
        self.assertIn(e2, positions)

if __name__ == '__main__':
    unittest.main()
