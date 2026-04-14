import unittest
import numpy as np
from src.nethawk.engine.ecs import World
from src.nethawk.components import Position, Item, Inventory
from src.nethawk.systems import inventory_system
from src.nethawk.events import PickupEvent, DropEvent

class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        self.world = World()
        self.actor = self.world.create_entity()
        self.item_entity = self.world.create_entity()

        # Add components to actor
        self.world.add_component(self.actor, Inventory())

        actor_pos = Position()
        actor_pos.set(5.0, 5.0)
        self.world.add_component(self.actor, actor_pos)

        # Add components to item
        self.world.add_component(self.item_entity, Item(name="Sword", weight=5.0))

        item_pos = Position()
        item_pos.set(5.0, 5.0)
        self.world.add_component(self.item_entity, item_pos)

    def test_pickup_event(self):
        # Push pickup event
        self.world.push_event(PickupEvent(actor=self.actor, item=self.item_entity))

        # Run system
        inventory_system(self.world)

        # Assert item is in inventory
        inventory = self.world.get_component(self.actor, Inventory)
        self.assertIn(self.item_entity, inventory.items)

        # Assert item position is removed
        self.assertFalse(self.world.has_component(self.item_entity, Position))

    def test_drop_event(self):
        # First pickup the item
        inventory = self.world.get_component(self.actor, Inventory)
        inventory.items.append(self.item_entity)
        self.world.remove_component(self.item_entity, Position)

        # Verify it's in inventory and has no position
        self.assertIn(self.item_entity, inventory.items)
        self.assertFalse(self.world.has_component(self.item_entity, Position))

        # Push drop event
        self.world.push_event(DropEvent(actor=self.actor, item=self.item_entity))

        # Run system
        inventory_system(self.world)

        # Assert item is no longer in inventory
        self.assertNotIn(self.item_entity, inventory.items)

        # Assert item has a position again
        self.assertTrue(self.world.has_component(self.item_entity, Position))

        # Assert the position is the same as the actor's position
        actor_pos = self.world.get_component(self.actor, Position)
        item_pos = self.world.get_component(self.item_entity, Position)

        self.assertAlmostEqual(actor_pos.x, item_pos.x)
        self.assertAlmostEqual(actor_pos.y, item_pos.y)

if __name__ == '__main__':
    unittest.main()
