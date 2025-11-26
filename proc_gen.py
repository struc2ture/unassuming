from __future__ import annotations

import random
from typing import Iterator, Tuple, List

import tcod

from entity import Entity
import templates
from tile_map import TileMap
import tile_types

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


class MapSpec:
    max_rooms: int
    room_min_size: int
    room_max_size: int
    map_width: int
    map_height: int
    max_monsters_per_room: int

    def __init__(
        self,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        max_monsters_per_room: int
    ):
        self.max_rooms = max_rooms
        self.room_min_size = room_min_size
        self.room_max_size = room_max_size
        self.map_width = map_width
        self.map_height = map_height
        self.max_monsters_per_room = max_monsters_per_room


def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def place_room_entities(
    room: RectangularRoom,
    entities: List[Entity],
    max_monsters: int,
    is_hostile_room: bool
) -> None:
    monster_count = random.randint(0, max_monsters)
    if is_hostile_room:
        for i in range(monster_count):
            x = random.randint(room.x1 + 1, room.x2 - 1)
            y = random.randint(room.y1 + 1, room.y2 - 1)

            if not any(entity.x == x and entity.y == y for entity in entities):
                if random.random() < 0.8:
                    entities.append(templates.CRANE.spawn(x, y))
                else:
                    entities.append(templates.BULB.spawn(x, y))
    else:
        npc_template = random.choice(templates.NPCS)

        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in entities):
            entities.append(npc_template.spawn(x, y))


def generate_map(
    spec: MapSpec,
    player: Entity,
    entities: List[Entity]
) -> TileMap:
    map = TileMap(spec.map_width, spec.map_height)

    rooms: List[RectangularRoom] = []

    for r in range(spec.max_rooms):
        room_w = random.randint(spec.room_min_size, spec.room_max_size)
        room_h = random.randint(spec.room_min_size, spec.room_max_size)

        x = random.randint(0, map.cols - room_w - 1)
        y = random.randint(0, map.rows - room_h - 1)

        new_room = RectangularRoom(x, y, room_w, room_h)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        map.tiles[new_room.inner] = tile_types.floor

        if len(rooms) > 0: # skip the first room
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                map.tiles[x, y] = tile_types.floor
            place_hostile = random.randint(0, 1) == 0
            place_room_entities(new_room, entities, spec.max_monsters_per_room, place_hostile)

        rooms.append(new_room)

    player.set_pos(*rooms[0].center)

    entities.append(templates.USHER.spawn(rooms[0].center[0], rooms[0].center[1] + 1))

    entities.append(templates.DAGGER.spawn(rooms[0].center[0], rooms[0].center[1] - 1))
    entities.append(templates.SWORD.spawn(rooms[0].center[0] - 1, rooms[0].center[1]))
    entities.append(templates.LEATHER_ARMOR.spawn(rooms[0].center[0] - 2, rooms[0].center[1]))
    entities.append(templates.A_TRINKET.spawn(rooms[0].center[0] + 1, rooms[0].center[1]))
    entities.append(templates.A_MAP.spawn(rooms[0].center[0] + 2, rooms[0].center[1]))

    return map
