import json
import dataclasses
from enum import Enum
from typing import Any, Dict, List
import numpy as np

class MessageType(Enum):
    JOIN = "JOIN"
    WELCOME = "WELCOME"
    MOVE = "MOVE"
    STATE = "STATE"
    ERROR = "ERROR"

def serialize(message_type: MessageType, payload: Dict[str, Any]) -> str:
    """Serializes a message to a JSON string."""
    data = {
        "type": message_type.value,
        "payload": payload
    }
    return json.dumps(data, default=_json_encoder)

def deserialize(data: str) -> Dict[str, Any]:
    """Deserializes a JSON string to a message dict."""
    return json.loads(data)

def _json_encoder(obj):
    """Custom JSON encoder for numpy arrays and other types."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
