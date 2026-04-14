import asyncio
import logging
import numpy as np
from typing import Dict, Set, List

from src.nethawk.engine.ecs import World, Entity
from src.nethawk.components import Position, Velocity, Identity
from src.nethawk.main import create_player
from src.nethawk.systems.movement import movement_system
from src.nethawk.network.protocol import MessageType, serialize, deserialize

logger = logging.getLogger(__name__)

class GameServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self.host = host
        self.port = port
        self.world = World()
        self.clients: Dict[asyncio.StreamWriter, Entity] = {}
        self.running = False

    async def start(self):
        """Starts the game server."""
        self.running = True
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        logger.info(f"Serving on {addr}")

        # The serve_forever loop needs to be concurrent with the game loop
        async with server:
            # We use asyncio.create_task for the game loop so it runs in background
            # while server.serve_forever() blocks and handles new connections.
            game_loop_task = asyncio.create_task(self.game_loop())
            try:
                await server.serve_forever()
            finally:
                self.running = False
                game_loop_task.cancel()
                try:
                    await game_loop_task
                except asyncio.CancelledError:
                    pass

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handles a new client connection."""
        addr = writer.get_extra_info('peername')
        logger.info(f"New connection from {addr}")

        # Create player entity
        player_entity = create_player(self.world)
        self.clients[writer] = player_entity

        # Send welcome message
        welcome_msg = serialize(MessageType.WELCOME, {"entity_id": player_entity})
        writer.write(welcome_msg.encode() + b'\n')
        await writer.drain()

        try:
            while self.running:
                data = await reader.readline()
                if not data:
                    break

                try:
                    message_str = data.decode().strip()
                    if not message_str:
                        continue
                    message = deserialize(message_str)
                    await self.process_message(player_entity, message)
                except Exception as e:
                    logger.error(f"Error processing message from {addr}: {e}")

        except ConnectionResetError:
            pass
        finally:
            logger.info(f"Connection closed from {addr}")
            self.clients.pop(writer, None)
            self.world.destroy_entity(player_entity)
            writer.close()
            await writer.wait_closed()

    async def process_message(self, entity: Entity, message: Dict):
        """Processes a message from a client."""
        msg_type = message.get("type")
        payload = message.get("payload", {})

        if msg_type == MessageType.MOVE.value:
            # Update velocity based on input
            # Payload expected: {"dx": float, "dy": float}
            dx = payload.get("dx", 0.0)
            dy = payload.get("dy", 0.0)

            # Simple validation/clamping could go here
            vel = self.world.get_component(entity, Velocity)
            if vel:
                vel.vector = np.array([dx, dy], dtype=np.float32)

    async def game_loop(self):
        """Main game loop running at a fixed tick rate."""
        tick_rate = 20  # Ticks per second
        dt = 1.0 / tick_rate

        while self.running:
            start_time = asyncio.get_event_loop().time()

            # Run systems
            movement_system(self.world, dt)

            # Broadcast state
            await self.broadcast_state()

            # Wait for next tick
            elapsed = asyncio.get_event_loop().time() - start_time
            sleep_time = max(0, dt - elapsed)
            await asyncio.sleep(sleep_time)

    async def broadcast_state(self):
        """Broadcasts the current world state to all clients."""
        if not self.clients:
            return

        # Gather state
        # For simplicity, we send all entities with Position
        positions = self.world.get_components(Position)
        identities = self.world.get_components(Identity)

        state_payload = []
        for entity, pos in positions.items():
            entity_data = {
                "id": entity,
                "x": pos.x,
                "y": pos.y
            }
            if entity in identities:
                entity_data["name"] = identities[entity].name
            state_payload.append(entity_data)

        message = serialize(MessageType.STATE, {"entities": state_payload})
        encoded_msg = message.encode() + b'\n'

        for writer in list(self.clients.keys()):
            if writer.is_closing():
                continue
            try:
                writer.write(encoded_msg)
                # We don't await drain here to avoid blocking the loop on slow clients
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
