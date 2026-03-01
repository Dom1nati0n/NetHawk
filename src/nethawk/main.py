import numpy as np
from .engine.ecs import World
from .components import Identity, Attributes, Status, Position, Velocity, Alignment, Gender
from .systems import movement_system, inventory_system

def create_player(world: World):
    """Creates the main player entity with components from the Guidebook."""
    player = world.create_entity()

    # Guidebook: Valkyries are hardy warrior women... strong... stealth and cunning.
    # Guidebook Figure 1: "Player the Rambler St:12 Dx:7 Co:18 In:11 Wi:9 Ch:15 Neutral"
    
    world.add_component(player, Identity(
        name="Player",
        role="Valkyrie",
        race="Human",
        gender=Gender.FEMALE,
        alignment=Alignment.NEUTRAL
    ))

    world.add_component(player, Attributes(
        strength=12,
        dexterity=7,
        constitution=18,
        intelligence=11,
        wisdom=9,
        charisma=15
    ))

    # Figure 1: "HP:9(12) Pw:3(3) AC:10 Exp:1/19 T:752 Hungry Conf"
    world.add_component(player, Status(
        hp=9,
        max_hp=12,
        power=3,
        max_power=3,
        ac=10,
        level=1,
        gold=993,
        exp=19,
        hunger=1 # Hungry state
    ))

    # Initial position
    pos = Position()
    pos.set(10, 10)
    world.add_component(player, pos)
    
    # Add velocity for movement system test
    vel = Velocity()
    vel.vector = np.array([1.0, 0.0], dtype=np.float32) # Moving East
    world.add_component(player, vel)

    return player

def main_loop():
    """Main simulation loop."""
    world = World()
    player = create_player(world)

    print("NetHawk Simulation Started.")
    print(f"Player Created: {world.get_component(player, Identity)}")
    print(f"Initial Position: {world.get_component(player, Position).coords}")

    # Simulation parameters
    total_time = 0.0
    dt = 1.0 # 1 second steps for simplicity in this demo
    max_steps = 5

    for step in range(max_steps):
        # Process Events & Systems
        inventory_system(world)

        # Physics / Movement System
        movement_system(world, dt)
        
        pos = world.get_component(player, Position)
        print(f"Step {step+1}: Time {total_time:.1f}s -> Player Position: {pos.coords}")
        
        # Clear events for the next tick
        world.clear_events()

        total_time += dt

if __name__ == "__main__":
    main_loop()
