import asyncio
import logging
from typing import Optional, Dict

from src.nethawk.network.protocol import MessageType, serialize, deserialize

logger = logging.getLogger(__name__)

class GameClient:
    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.running = False
        self.my_entity_id: Optional[int] = None
        self.world_state: Dict = {}

    async def connect(self):
        """Connects to the game server."""
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            logger.info(f"Connected to {self.host}:{self.port}")
            self.running = True

            # Start listening loop
            await self.listen_loop()
        except Exception as e:
            logger.error(f"Failed to connect: {e}")

    async def listen_loop(self):
        """Listens for messages from the server."""
        try:
            while self.running and self.reader:
                data = await self.reader.readline()
                if not data:
                    break

                try:
                    message_str = data.decode().strip()
                    if not message_str:
                        continue
                    message = deserialize(message_str)
                    await self.process_message(message)
                except Exception as e:
                    logger.error(f"Error processing server message: {e}")

        except ConnectionResetError:
            logger.info("Connection lost.")
        finally:
            await self.disconnect()

    async def process_message(self, message: Dict):
        """Processes a message from the server."""
        msg_type = message.get("type")
        payload = message.get("payload", {})

        if msg_type == MessageType.WELCOME.value:
            self.my_entity_id = payload.get("entity_id")
            logger.info(f"Joined game. My Entity ID: {self.my_entity_id}")

        elif msg_type == MessageType.STATE.value:
            # Update local world state representation
            self.world_state = payload
            # For now, just print the state to see updates
            # In a real game, this would update local ECS or rendering
            entities = payload.get("entities", [])
            # logger.debug(f"Received state update for {len(entities)} entities")
            # print(f"State: {entities}")

    async def send_move(self, dx: float, dy: float):
        """Sends a move command to the server."""
        if not self.writer:
            return

        message = serialize(MessageType.MOVE, {"dx": dx, "dy": dy})
        try:
            self.writer.write(message.encode() + b'\n')
            await self.writer.drain()
        except Exception as e:
            logger.error(f"Error sending move: {e}")

    async def disconnect(self):
        """Disconnects from the server."""
        self.running = False
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.writer = None
            self.reader = None
        logger.info("Disconnected.")
