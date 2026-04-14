import numpy as np
import asyncio
import sys
import logging
import argparse
import random

from .engine.ecs import World
from .components import Identity, Attributes, Status, Position, Velocity, Alignment, Gender, Race, Role
from .systems import movement_system

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def create_player(world: World):
    """Creates the main player entity with components from the Guidebook."""
    player = world.create_entity()

    # Guidebook: Valkyries are hardy warrior women... strong... stealth and cunning.
    # Guidebook Figure 1: "Player the Rambler St:12 Dx:7 Co:18 In:11 Wi:9 Ch:15 Neutral"
    
    world.add_component(player, Identity(
        name="Player",
        role=Role.VALKYRIE,
        race=Race.HUMAN,
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
    
    # Add velocity for movement system test (initially zero)
    vel = Velocity()
    vel.vector = np.array([0.0, 0.0], dtype=np.float32)
    world.add_component(player, vel)

    return player

def run_simulation():
    """Main simulation loop (Standalone Mode)."""
    world = World()
    player = create_player(world)

    # Add initial velocity for demo
    vel = world.get_component(player, Velocity)
    vel.vector = np.array([1.0, 0.0], dtype=np.float32)

    print("NetHawk Simulation Started.")
    print(f"Player Created: {world.get_component(player, Identity)}")
    print(f"Initial Position: {world.get_component(player, Position).coords}")

    # Simulation parameters
    total_time = 0.0
    dt = 1.0 # 1 second steps for simplicity in this demo
    max_steps = 5

    for step in range(max_steps):
        # Physics / Movement System
        movement_system(world, dt)
        
        pos = world.get_component(player, Position)
        print(f"Step {step+1}: Time {total_time:.1f}s -> Player Position: {pos.coords}")
        
        total_time += dt

async def run_server(host, port):
    from .network.server import GameServer
    server = GameServer(host, port)
    await server.start()

async def run_client(host, port):
    from .network.client import GameClient
    client = GameClient(host, port)

    # Connect in background task
    connection_task = asyncio.create_task(client.connect())

    # Simple input loop for demo purposes
    # In a real game this would be driven by UI events
    print("Client started. Type 'w/a/s/d' to move, 'q' to quit.")

    # Wait for connection to establish
    await asyncio.sleep(1)

    try:
        while client.running:
            # Non-blocking input handling is tricky in standard terminal without curses/libraries
            # For this simple demo, we'll just wait a bit and simulate some movement or check state

            # Here we just print the latest state periodically
            if client.world_state:
                print(f"Current State: {client.world_state}")

            # Demo: Random movement
            dx = random.choice([-1.0, 0.0, 1.0])
            dy = random.choice([-1.0, 0.0, 1.0])
            if dx != 0 or dy != 0:
                 await client.send_move(dx, dy)

            await asyncio.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        await client.disconnect()

def main():
    parser = argparse.ArgumentParser(description="NetHawk Game")
    subparsers = parser.add_subparsers(dest="mode", help="Mode: server, client, or simulation (default)")

    # Server parser
    server_parser = subparsers.add_parser("server", help="Run as game server")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    server_parser.add_argument("--port", type=int, default=8080, help="Port to bind to")

    # Client parser
    client_parser = subparsers.add_parser("client", help="Run as game client")
    client_parser.add_argument("--host", default="127.0.0.1", help="Server host")
    client_parser.add_argument("--port", type=int, default=8080, help="Server port")

    # Simulation parser (default behavior)
    sim_parser = subparsers.add_parser("simulation", help="Run standalone simulation")

    args = parser.parse_args()

    if args.mode == "server":
        asyncio.run(run_server(args.host, args.port))
    elif args.mode == "client":
        asyncio.run(run_client(args.host, args.port))
    else:
        run_simulation()

if __name__ == "__main__":
    main()
