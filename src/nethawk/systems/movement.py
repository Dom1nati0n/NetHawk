from ..engine.ecs import World
from ..components.spatial import Position, Velocity

def movement_system(world: World, dt: float):
    """Updates entity positions based on their velocity."""
    
    # Get all entities with both Position and Velocity components
    positions = world.get_components(Position)
    velocities = world.get_components(Velocity)

    # Intersection of entities having both
    entities = set(positions.keys()) & set(velocities.keys())

    for entity in entities:
        pos = positions[entity]
        vel = velocities[entity]

        # Update position
        # We now use floats to accumulate sub-grid movement
        # pos.coords is float32, vel.vector is float32
        
        # Simple Euler integration: p' = p + v * dt
        pos.coords += vel.vector * dt
