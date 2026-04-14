import numpy as np
from ..engine.ecs import World
from ..events import PickupEvent, DropEvent
from ..components.inventory import Inventory, Item
from ..components.spatial import Position

def inventory_system(world: World):
    """Processes inventory-related events like picking up and dropping items."""

    # Process PickupEvents
    pickup_events = world.get_events(PickupEvent)
    for event in pickup_events:
        actor = event.actor
        item_entity = event.item

        # Verify actor has an inventory and item is an Item
        if not world.has_component(actor, Inventory):
            continue
        if not world.has_component(item_entity, Item):
            continue

        inventory = world.get_component(actor, Inventory)

        # We could check weight capacity here in the future
        inventory.items.append(item_entity)

        # Remove Position component from item since it's now in inventory
        if world.has_component(item_entity, Position):
            world.remove_component(item_entity, Position)

    # Process DropEvents
    drop_events = world.get_events(DropEvent)
    for event in drop_events:
        actor = event.actor
        item_entity = event.item

        # Verify actor has an inventory and position
        if not world.has_component(actor, Inventory):
            continue
        if not world.has_component(actor, Position):
            continue

        inventory = world.get_component(actor, Inventory)

        # Ensure item is actually in inventory
        if item_entity not in inventory.items:
            continue

        inventory.items.remove(item_entity)

        # Place item at actor's position
        actor_pos = world.get_component(actor, Position)

        new_item_pos = Position()
        # Ensure we copy the coordinates rather than sharing the reference
        new_item_pos.coords = np.copy(actor_pos.coords)

        world.add_component(item_entity, new_item_pos)
