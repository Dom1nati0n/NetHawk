import unittest
import numpy as np
from src.nethawk.engine.ecs import World
from src.nethawk.components import Position, Velocity, Identity, Attributes
from src.nethawk.systems.movement import movement_system

class TestNetHawk(unittest.TestCase):
    def setUp(self):
        self.world = World()
        self.player = self.world.create_entity()

    def test_entity_creation_and_components(self):
        # Create components
        pos = Position()
        vel = Velocity()
        identity = Identity(name="Player", role="Val", race="Hum", gender=1, alignment=0)
        
        self.world.add_component(self.player, pos)
        self.world.add_component(self.player, vel)
        self.world.add_component(self.player, identity)

        # Check existence
        self.assertTrue(self.world.has_component(self.player, Position))
        self.assertTrue(self.world.has_component(self.player, Identity))
        self.assertFalse(self.world.has_component(self.player, Attributes))

        # Check retrieval
        p = self.world.get_component(self.player, Position)
        self.assertIsInstance(p, Position)
        self.assertAlmostEqual(p.x, 0.0)

    def test_movement_system(self):
        pos = Position()
        pos.set(10.0, 10.0)
        
        vel = Velocity()
        vel.vector = np.array([1.0, 0.0]) # 1 unit/sec East
        
        self.world.add_component(self.player, pos)
        self.world.add_component(self.player, vel)

        # Step 1: dt=0.5 -> Move 0.5 units (Precision test)
        movement_system(self.world, 0.5)
        
        updated_pos = self.world.get_component(self.player, Position)
        self.assertAlmostEqual(updated_pos.x, 10.5)
        self.assertAlmostEqual(updated_pos.y, 10.0)
        self.assertEqual(updated_pos.grid_x, 10) # Truncated for grid rendering

        # Step 2: dt=0.5 -> Move another 0.5 units -> total 1.0 unit
        movement_system(self.world, 0.5)
        
        updated_pos = self.world.get_component(self.player, Position)
        self.assertAlmostEqual(updated_pos.x, 11.0)
        self.assertAlmostEqual(updated_pos.y, 10.0)
        self.assertEqual(updated_pos.grid_x, 11)

if __name__ == '__main__':
    unittest.main()
