from __future__ import annotations
from typing import TYPE_CHECKING

import tcod
from tcod.context import Context
from tcod.event import Event

from game_logic import GameLogic
from game_state import GameState
from game_intent import GameIntent

if TYPE_CHECKING:
    from game_app import GameApp

class PickTargetState(GameState):
    def __init__(self, game_logic: GameLogic, game_app: GameApp, parent_console: tcod.console.Console, for_intent: GameIntent):
        super().__init__(game_logic, game_app)
        self.parent_console = parent_console
        self.for_intent = for_intent
        self.cursor_x = self.game_logic.player.x
        self.cursor_y = self.game_logic.player.y

    def render(self, parent_console: tcod.console.Console) -> None:
        parent_console.print(
            self.cursor_x,
            self.cursor_y,
            text="x"
        )

    def move_cursor(self, dx: int, dy: int) -> None:
        self.cursor_x += dx
        self.cursor_y += dy
        if self.cursor_x < 0:
            self.cursor_x = 0
        if self.cursor_x >= self.parent_console.width:
            self.cursor_x = self.parent_console.width - 1
        if self.cursor_y < 0:
            self.cursor_y = 0
        if self.cursor_y >= self.parent_console.height:
            self.cursor_y = self.parent_console.height - 1

    def handle_event(self, context: Context, event: Event) -> None:
        match event:
            case tcod.event.KeyDown(sym=tcod.event.KeySym.X):
                self.move_cursor( 0, +1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.W):
                self.move_cursor( 0, -1)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.A):
                self.move_cursor(-1,  0)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.D):
                self.move_cursor(+1,  0)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RETURN):
                # TODO(A): The idea was that a state like this ("function-return" type) should not write through game logic.
                #          But here needs to be a mechanism to return data when popping state, so the GameApp itself can orchestrate it.
                #          This UI state should also not have the reference to the intent this is for. (Could be not for any intent.)
                self.for_intent.target = (self.cursor_x, self.cursor_y)
                self.game_logic.process_intent(self.for_intent)
                self.game_app.pop_state()
