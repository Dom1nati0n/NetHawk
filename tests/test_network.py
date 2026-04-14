import unittest
import sys
import json
import asyncio
import logging

# --- MOCK NUMPY SETUP START ---
# We define our mocks BEFORE importing any application code
from unittest.mock import MagicMock

class MockArray:
    def __init__(self, data, dtype=None):
        self.data = list(data)
        self.dtype = dtype

    def tolist(self):
        return self.data

    def item(self):
        if len(self.data) == 1:
            return self.data[0]
        raise ValueError("item() called on multi-element array")

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, value):
        self.data[idx] = value

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return f"MockArray({self.data})"

    def __add__(self, other):
        if hasattr(other, 'data'):
            return MockArray([a + b for a, b in zip(self.data, other.data)])
        return MockArray([a + other for a in self.data])

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if hasattr(other, 'data'):
            return MockArray([a * b for a, b in zip(self.data, other.data)])
        return MockArray([a * other for a in self.data])

    def __rmul__(self, other):
        return self.__mul__(other)

# Inject mock numpy into sys.modules
mock_np = MagicMock()
mock_np.array = lambda data, dtype=None: MockArray(data, dtype)
mock_np.zeros = lambda shape, dtype=None: MockArray([0.0]*shape if isinstance(shape, int) else [0.0]*shape[0], dtype)
mock_np.float32 = float
sys.modules["numpy"] = mock_np
# --- MOCK NUMPY SETUP END ---

# Now import application modules
from src.nethawk.network.protocol import MessageType, serialize, deserialize
from src.nethawk.network.server import GameServer
from src.nethawk.network.client import GameClient
from src.nethawk.components import Velocity

class TestNetworkProtocol(unittest.TestCase):
    def test_serialization(self):
        payload = {"x": 10.5, "y": 20.0, "name": "Test"}
        serialized = serialize(MessageType.MOVE, payload)

        data = json.loads(serialized)
        self.assertEqual(data["type"], "MOVE")
        self.assertEqual(data["payload"]["x"], 10.5)

    def test_deserialization(self):
        json_str = '{"type": "JOIN", "payload": {"id": 1}}'
        data = deserialize(json_str)
        self.assertEqual(data["type"], "JOIN")
        self.assertEqual(data["payload"]["id"], 1)

class TestGameServerClient(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.server_port = 9001
        self.server = GameServer(port=self.server_port)
        self.server_task = asyncio.create_task(self.server.start())
        await asyncio.sleep(0.1) # Wait for server to bind

    async def asyncTearDown(self):
        self.server.running = False
        self.server_task.cancel()
        try:
            await self.server_task
        except asyncio.CancelledError:
            pass

    async def test_client_connect_and_move(self):
        client = GameClient(port=self.server_port)

        # Connect
        connect_task = asyncio.create_task(client.connect())
        await asyncio.sleep(0.1)
        self.assertTrue(client.running)

        # Wait for handshake (WELCOME)
        await asyncio.sleep(0.1)
        self.assertIsNotNone(client.my_entity_id)

        # Send MOVE
        await client.send_move(5.0, 5.0)
        await asyncio.sleep(0.2)

        # Check server state
        entity_id = client.my_entity_id
        vel = self.server.world.get_component(entity_id, Velocity)

        self.assertIsNotNone(vel, "Velocity component missing on server entity")
        self.assertEqual(vel.vector[0], 5.0)
        self.assertEqual(vel.vector[1], 5.0)

        # Cleanup client
        await client.disconnect()
        try:
            await connect_task
        except:
            pass

if __name__ == '__main__':
    logging.disable(logging.CRITICAL) # Silence logs during test
    unittest.main()
