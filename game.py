from typing import List, Optional

import tcod

from entity import Entity
import entity_specs
from game_map import GameMap
import proc_gen

class Game:
    player: Entity
    game_map: GameMap
    entities: List[Entity]

    def __init__(self, map_width: int, map_height: int):
        self.player = Entity(entity_specs.player, 0, 0)
        self.entities = [self.player]

        map_spec = proc_gen.MapSpec(
            max_rooms=30,
            room_min_size=6,
            room_max_size=10,
            map_width=map_width,
            map_height=map_height,
            max_monsters_per_room=2
        )   
        self.game_map = proc_gen.generate_map(
            map_spec,
            player=self.player,
            entities=self.entities
        )
        self.update_fov()

    def handle_event(self, event: tcod.event.Event) -> None:
        player_dx = 0
        player_dy = 0
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                raise SystemExit

            case tcod.event.KeyDown(sym=tcod.event.KeySym.A):
                player_dx = -1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.D):
                player_dx = +1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.W):
                player_dy = -1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.S):
                player_dy = +1

        self.move_entity(self.player, player_dx, player_dy)

    def draw(self, console: tcod.console.Console) -> None:
        self.game_map.draw(console)
        for entity in self.entities:
            if self.game_map.pos_visible(*entity.pos):
                entity.draw(console)

    def get_entity_at(self, x: int, y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return entity
        
        return None

    def move_entity(self, entity: Entity, dx: int, dy: int) -> None:
        new_x = entity.x + dx
        new_y = entity.y + dy
        if (
            self.game_map.pos_walkable(new_x, new_y) and
            self.get_entity_at(new_x, new_y) is None
        ):
            entity.set_pos(new_x, new_y)
        self.update_fov()

    def update_fov(self) -> None:
        self.game_map.visible[:] = tcod.map.compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        self.game_map.explored |= self.game_map.visible
