import numpy as np
from ..components.map import LevelMap, WALL, FLOOR

def generate_dungeon(width: int, height: int, min_room_size=3, max_room_size=8, num_attempts=20) -> LevelMap:
    """
    Generates a simple dungeon map.
    Optimized with numpy slicing for room carving and corridor drawing.
    """
    level = LevelMap(width, height)

    rooms = []

    # Attempt to place rooms
    for _ in range(num_attempts):
        w = np.random.randint(min_room_size, max_room_size + 1)
        h = np.random.randint(min_room_size, max_room_size + 1)

        # Ensure room is within bounds
        if width - w - 1 <= 1 or height - h - 1 <= 1:
            continue

        x = np.random.randint(1, width - w - 1)
        y = np.random.randint(1, height - h - 1)

        # Optimization: Check for overlap using slicing instead of nested loops
        region = level.tiles[y:y+h, x:x+w]
        if np.any(region == FLOOR):
            continue

        # Optimization: Carve room using numpy slicing
        level.tiles[y:y+h, x:x+w] = FLOOR
        rooms.append((x, y, w, h))

    # Connect rooms with corridors
    for i in range(len(rooms) - 1):
        x1, y1, w1, h1 = rooms[i]
        x2, y2, w2, h2 = rooms[i+1]

        # Calculate center points
        cx1, cy1 = x1 + w1 // 2, y1 + h1 // 2
        cx2, cy2 = x2 + w2 // 2, y2 + h2 // 2

        # Draw L-shaped corridor
        # Horizontal segment: (cx1, cy1) to (cx2, cy1)
        start_x, end_x = min(cx1, cx2), max(cx1, cx2)
        level.tiles[cy1, start_x:end_x + 1] = FLOOR

        # Vertical segment: (cx2, cy1) to (cx2, cy2)
        start_y, end_y = min(cy1, cy2), max(cy1, cy2)
        level.tiles[start_y:end_y + 1, cx2] = FLOOR

    return level
