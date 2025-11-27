
import datetime
import os

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
from in_game_log import InGameLog

class GameApp:
    game_turn: int
    game_logic: GameLogic
    actor_controller: ActorController
    state_stack: list[GameState]
    main_console: tcod.console.Console
    DEBUG_disable_in_game_log: bool

    def __init__(self, map_width: int, map_height: int, main_console: tcod.console.Console):
        self.main_console = main_console
        self.state_stack = []
        self.game_turn = 0

        self.game_logic = GameLogic(map_width, map_height)

        self.actor_controller = ActorController(self.game_logic)

        InGameLog.add_message("I hope you like it here! :)")
        InGameLog.add_message("I sure don't.")

        GameTrace.add_game_start()
        GameTrace.add_tick(self.game_turn)

        self.game_logic.tile_map.DEBUG_toggle_ignore_fov()
        self.DEBUG_disable_in_game_log = False

    def handle_event(self, context: tcod.context.Context, event: tcod.event.Event) -> None:
        context.convert_event(event)  # Adds tile coordinates to mouse events.
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                if self.state_stack:
                    self.pop_state()
                else:
                    raise SystemExit

        if self.state_stack:
            self.state_stack[-1].handle_event(context, event)
            return

        match event:
            case tcod.event.KeyDown(sym=tcod.event.KeySym.F1):
                if event.mod & tcod.event.Modifier.SHIFT:
                    dump_game_trace_to_file()
                else:
                    print()
                    GameTrace.log.print_last(5)
                    print()
            case tcod.event.KeyDown(sym=tcod.event.KeySym.F2):
                self.game_logic.tile_map.DEBUG_toggle_ignore_fov()
            case tcod.event.KeyDown(sym=tcod.event.KeySym.F3):
                self.DEBUG_disable_in_game_log = not self.DEBUG_disable_in_game_log
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
        self.state_stack.pop()

    def push_state(self, state: GameState):
        self.state_stack.append(state)

    # TODO(A): Shouldn't be here
    def draw_in_game_log(self, console: tcod.console.Console) -> None:
        console.draw_frame(
            0,
            console.height - 5,
            console.width,
            5,
            decoration="         ",
            bg=(0, 0, 0)
        )
        cursor_x = 0
        cursor_y = console.height - 5
        for message in InGameLog.log.messages[-5:]:
            console.print(
                cursor_x,
                cursor_y,
                text=message,
            )
            cursor_y += 1

    def draw(self, console: tcod.console.Console) -> None:
        self.game_logic.tile_map.draw(console)

        sorted_entities = sorted(
            self.game_logic.entities, key=lambda x: x.render_layer.value
        )
        for entity in sorted_entities:
            if self.game_logic.tile_map.pos_visible(*entity.pos):
                entity.draw(console)

        if not self.DEBUG_disable_in_game_log:
            self.draw_in_game_log(console)

        for state in self.state_stack:
            state.render(console)

def dump_game_trace_to_file():
    if not os.path.exists("log"):
        os.makedirs("log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"log/game_trace_{timestamp}.log"
    with open(filename, "w") as f:
        f.write(GameTrace.log.get_str())
