from ..engine.ecs import World
from ..components.spatial import Position, Velocity

def movement_system(world: World, dt: float):
    """Updates entity positions based on their velocity."""
    
    # Get all entities with both Position and Velocity components
    positions = world.get_components(Position)
    velocities = world.get_components(Velocity)

    # Intersection of entities having both
    # Optimization: iterate over the smaller dict to avoid extra set allocations
    if len(positions) < len(velocities):
        for entity, pos in positions.items():
            if entity in velocities:
                vel = velocities[entity]
                # Update position
                # Simple Euler integration: p' = p + v * dt
                pos.coords += vel.vector * dt
    else:
        for entity, vel in velocities.items():
            if entity in positions:
                pos = positions[entity]
                # Update position
                # Simple Euler integration: p' = p + v * dt
                pos.coords += vel.vector * dt
