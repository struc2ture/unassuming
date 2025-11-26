
import datetime
import os
from typing import List, Optional

import tcod

from actor_controller import ActorController
from entity import Actor
from game_effect import *
from game_logic import GameLogic
from game_trace import GameTrace
from game_state import GameState
from inspect_state import InspectState
from inventory_state import InventoryState
from dialog_state import DialogState

class GameApp:
    game_turn: int
    game_logic: GameLogic
    actor_controller: ActorController
    current_state: Optional[GameState]
    main_console: tcod.console.Console

    def __init__(self, map_width: int, map_height: int, main_console: tcod.console.Console):
        self.main_console = main_console
        self.current_state = None
        self.game_turn = 0

        self.game_logic = GameLogic(map_width, map_height)

        self.actor_controller = ActorController(self.game_logic)

        GameTrace.add_game_start()
        GameTrace.add_tick(self.game_turn)


    def handle_event(self, context: tcod.context.Context, event: tcod.event.Event) -> None:
        context.convert_event(event)  # Adds tile coordinates to mouse events.
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                if self.current_state:
                    self.current_state = None
                else:
                    raise SystemExit

        if self.current_state:
            self.current_state.handle_event(context, event)
            return

        match event:
            case tcod.event.KeyDown(sym=tcod.event.KeySym.L):
                if event.mod & tcod.event.Modifier.SHIFT:
                    dump_game_trace_to_file()
                else:
                    print()
                    GameTrace.log.print_last(5)
                    print()
            case tcod.event.MouseButtonDown(button=tcod.event.MouseButton.LEFT, tile=tile):
                entity = self.game_logic.get_entities_at(int(tile.x), int(tile.y))
                if entity:
                    self.push_state(InspectState(self.game_logic, self, self.main_console, entity[0]))

        player_dx = 0
        player_dy = 0
        player_passed_turn = False

        if self.game_logic.player.is_alive:
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
                    self.game_logic.skip_turn(self.game_logic.player)
                    player_passed_turn = True

                case tcod.event.KeyDown(sym=tcod.event.KeySym.G):
                    self.game_logic.pickup_item_below(self.game_logic.player)
                    print(", ".join(item.name for item in self.game_logic.player.inventory))
                    player_passed_turn = True

                case tcod.event.KeyDown(sym=tcod.event.KeySym.V):
                    self.game_logic.drop_item(self.game_logic.player)
                    player_passed_turn = True

                case tcod.event.KeyDown(sym=tcod.event.KeySym.I):
                    self.push_state(InventoryState(self.game_logic, self, self.main_console, self.game_logic.player))

            if player_dx != 0 or player_dy != 0:
                effects = self.game_logic.player_move_or_bump(self.game_logic.player, player_dx, player_dy)
                for effect in effects:
                    match effect:
                        case StartDialogGameEffect(with_actor=with_actor):
                            self.push_state(DialogState(self.game_logic, self, self.main_console, with_actor))
                player_passed_turn = True

            if player_passed_turn:
                for entity in self.game_logic.entities:
                    # print(f'Processing entity {entity.name}. Actor: {isinstance(entity, Actor)}. Alive: {isinstance(entity, Actor) and entity.is_alive}')
                    if isinstance(entity, Actor) and entity is not self.game_logic.player and entity.is_alive:
                        self.actor_controller.process_actor_turn(entity)

                self.game_turn += 1
                GameTrace.add_tick(self.game_turn)

    def pop_state(self):
        self.current_state = None

    def push_state(self, state: GameState):
        self.current_state = state

    def draw(self, console: tcod.console.Console) -> None:
        self.game_logic.tile_map.draw(console)
        sorted_entities = sorted(
            self.game_logic.entities, key=lambda x: x.render_layer.value
        )
        for entity in sorted_entities:
            if self.game_logic.tile_map.pos_visible(*entity.pos):
                entity.draw(console)

        if self.current_state:
            self.current_state.render(console)

def dump_game_trace_to_file():
    if not os.path.exists("log"):
        os.makedirs("log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"log/game_trace_{timestamp}.log"
    with open(filename, "w") as f:
        f.write(GameTrace.log.get_str())
