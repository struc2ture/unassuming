import datetime
import os
from typing import List, Optional

import tcod

from entity import Actor, Entity
from entity_controller import EntityController
import templates
from game_map import GameMap
from game_trace import GameTrace
import proc_gen

class Game:
    player: Actor
    game_map: GameMap
    entities: List[Entity]
    entity_controller: EntityController

    def __init__(self, map_width: int, map_height: int):
        self.game_turn = 0

        GameTrace.add_game_start()
        GameTrace.add_tick(self.game_turn)

        self.player = templates.PLAYER.spawn(0, 0)
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

        self.entity_controller = EntityController(game_map=self.game_map, entities=self.entities, player=self.player)

        self.update_fov()

    def handle_event(self, context: tcod.context.Context, event: tcod.event.Event) -> None:
        context.convert_event(event)  # Adds tile coordinates to mouse events.
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                raise SystemExit
            case tcod.event.KeyDown(sym=tcod.event.KeySym.L):
                if event.mod & tcod.event.Modifier.SHIFT:
                    dump_game_trace_to_file()
                else:
                    print()
                    GameTrace.log.print_last(5)
                    print()
            case tcod.event.MouseButtonDown(button=tcod.event.MouseButton.LEFT, tile=tile):
                entity = self.entity_controller.get_entity_at(int(tile.x), int(tile.y))
                if entity:
                    print("\nCLICKED ENTITY:")
                    print(entity.name)
                    print(entity.description)
                    print()
        
        player_dx = 0
        player_dy = 0
        player_passed_turn = False

        if self.player.is_alive:
            match event:
                case tcod.event.KeyDown(sym=tcod.event.KeySym.Q):
                    player_dx = -1
                    player_dy = -1
                case tcod.event.KeyDown(sym=tcod.event.KeySym.W):
                    player_dx =  0
                    player_dy = -1
                case tcod.event.KeyDown(sym=tcod.event.KeySym.E):
                    player_dx = +1
                    player_dy = -1
                case tcod.event.KeyDown(sym=tcod.event.KeySym.D):
                    player_dx = +1
                    player_dy =  0
                case tcod.event.KeyDown(sym=tcod.event.KeySym.C):
                    player_dx = +1
                    player_dy = +1
                case tcod.event.KeyDown(sym=tcod.event.KeySym.X):
                    player_dx =  0
                    player_dy = +1
                case tcod.event.KeyDown(sym=tcod.event.KeySym.Z):
                    player_dx = -1
                    player_dy = +1
                case tcod.event.KeyDown(sym=tcod.event.KeySym.A):
                    player_dx = -1
                    player_dy =  0
                case tcod.event.KeyDown(sym=tcod.event.KeySym.S):
                    self.entity_controller.skip_turn(self.player)
                    player_passed_turn = True

            if player_dx != 0 or player_dy != 0:
                self.entity_controller.player_move_or_bump(self.player, player_dx, player_dy)
                self.update_fov()
                player_passed_turn = True

            if player_passed_turn:
                self.entity_controller.process_entity_turns()
                self.game_turn += 1
                GameTrace.add_tick(self.game_turn)


    def draw(self, console: tcod.console.Console) -> None:
        self.game_map.draw(console)
        sorted_entities = sorted(
            self.entities, key=lambda x: x.render_layer.value
        )
        for entity in sorted_entities:
            if self.game_map.pos_visible(*entity.pos):
                entity.draw(console)

    def update_fov(self) -> None:
        self.game_map.visible[:] = tcod.map.compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        self.game_map.explored |= self.game_map.visible

def dump_game_trace_to_file():
    if not os.path.exists("log"):
        os.makedirs("log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"log/game_trace_{timestamp}.log"
    with open(filename, "w") as f:
        f.write(GameTrace.log.get_str())
