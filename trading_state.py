from __future__ import annotations
from typing import TYPE_CHECKING

import textwrap
from typing import Tuple

import tcod
from tcod.context import Context
from tcod.event import Event

from entity import Actor, Item
from game_state import GameState
from game_logic import GameLogic

if TYPE_CHECKING:
    from game_app import GameApp

class TradingState(GameState):
    def __init__(self, game_logic: GameLogic, game_app: GameApp, parent_console: tcod.console.Console, requesting_actor: Actor, responding_actor: Actor):
        super().__init__(game_logic, game_app)
        self.width: int = 50
        self.height: int = 40
        self.this_console: tcod.console.Console = tcod.console.Console(self.width, self.height)
        self.anchor: Tuple[int, int] = (parent_console.width // 2, parent_console.height // 2)
        self.offset: Tuple[int, int] = (-self.width // 2, -self.height // 2)
        self.requesting_actor: Actor = requesting_actor
        self.responding_actor: Actor = responding_actor
        self.selected_x = 0
        self.selected_y = 0
        self.selected_item_a: Item | None = None
        self.selected_item_b: Item | None = None

    def render(self, parent_console: tcod.console.Console) -> None:
        self.this_console.draw_frame(
            0,
            0,
            self.this_console.width,
            self.this_console.height,
            decoration="┼─┼│ │┼─┼"
        )
        self.this_console.draw_frame(
            self.this_console.width // 2,
            1,
            width=1,
            height=self.this_console.height - 2,
            decoration="┼─┼│ │┼─┼"
        )
        self.this_console.print(
            0,
            0,
            width=self.this_console.width,
            height=1,
            text="┤Trade├",
            alignment=tcod.constants.CENTER
        )

        cursor_x = 1
        cursor_y = 2

        self.this_console.print(
            cursor_x,
            cursor_y,
            text=f"{self.responding_actor.name}:"
        )
        
        cursor_y += 2

        index = 0
        for item in self.responding_actor.inventory:
            if self.selected_x == 0 and index == self.selected_y:
                bg=(255, 255, 255)
                fg=(0, 0, 0)
            else:
                bg=(0, 0, 0)
                fg=(255, 255, 255)
            self.this_console.print(
                cursor_x,
                cursor_y,
                text=f"  {item.name}",
                fg=fg,
                bg=bg
            )
            self.this_console.print(
                cursor_x,
                cursor_y,
                text=item.glyph,
                fg=item.color
            )
            cursor_y += 1
            index += 1

        cursor_y += 1

        if self.selected_item_a:
            self.this_console.print(
                cursor_x,
                self.this_console.height - 2,
                text=f"Selected:   {self.selected_item_a.name}",
            )
            self.this_console.print(
                cursor_x + len("Selected: "),
                self.this_console.height - 2,
                text=self.selected_item_a.glyph,
                fg=self.selected_item_a.color
            )
        

        cursor_x = self.width // 2 + 1
        cursor_y = 2

        self.this_console.print(
            cursor_x,
            cursor_y,
            text=f"{self.requesting_actor.name}:"
        )

        cursor_y += 2

        index = 0
        for item in self.requesting_actor.inventory:
            if self.selected_x == 1 and index == self.selected_y:
                bg=(255, 255, 255)
                fg=(0, 0, 0)
            else:
                bg=(0, 0, 0)
                fg=(255, 255, 255)
            self.this_console.print(
                cursor_x,
                cursor_y,
                text=f"  {item.name}",
                fg=fg,
                bg=bg
            )
            self.this_console.print(
                cursor_x,
                cursor_y,
                text=item.glyph,
                fg=item.color
            )
            cursor_y += 1
            index += 1

        if self.selected_item_b:
            self.this_console.print(
                cursor_x,
                self.this_console.height - 2,
                text=f"Selected:   {self.selected_item_b.name}",
            )
            self.this_console.print(
                cursor_x + len("Selected: "),
                self.this_console.height - 2,
                text=self.selected_item_b.glyph,
                fg=self.selected_item_b.color
            )

        self.this_console.blit(parent_console, self.anchor[0] + self.offset[0], self.anchor[1] + self.offset[1], bg_alpha=0.9)

    def move_cursor(self, dx: int, dy: int) -> None:
        self.selected_x = (self.selected_x + dx) % 2

        column_items = len(self.responding_actor.inventory) if self.selected_x == 0 else len(self.requesting_actor.inventory)
        self.selected_y = (self.selected_y + dy) % column_items
        
    def select_item(self, x: int, y: int) -> None:
        if x == 0:
            if self.selected_item_a == self.responding_actor.inventory[y]:
                self.selected_item_a = None
            else:
                self.selected_item_a = self.responding_actor.inventory[y]
        elif x == 1:
            if self.selected_item_b == self.requesting_actor.inventory[y]:
                self.selected_item_b = None
            else:
                self.selected_item_b = self.requesting_actor.inventory[y]

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
            case tcod.event.KeyDown(sym=tcod.event.KeySym.E):
                self.select_item(self.selected_x, self.selected_y)
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RETURN):
                if self.selected_item_a and self.selected_item_b:
                    self.game_logic.trade_items(self.responding_actor, self.requesting_actor, self.selected_item_a, self.selected_item_b)
                    self.game_app.pop_state()
