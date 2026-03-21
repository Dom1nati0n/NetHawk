import unittest
import sys

from src.nethawk.engine.ecs import World, EntityManager

class TestECS(unittest.TestCase):
    def test_entity_manager_recycle(self):
        manager = EntityManager()
        id1 = manager.create_entity()
        id2 = manager.create_entity()
        self.assertEqual(id1, 0)
        self.assertEqual(id2, 1)

        manager.destroy_entity(id1)

        # Next created entity should reuse id1
        id3 = manager.create_entity()
        self.assertEqual(id3, id1)

    def test_entity_manager_maxsize(self):
        manager = EntityManager()
        # Mock next_id to be maxsize
        manager._next_id = sys.maxsize

        with self.assertRaises(RuntimeError):
            manager.create_entity()

if __name__ == '__main__':
    unittest.main()
