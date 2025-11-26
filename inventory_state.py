from __future__ import annotations
from typing import TYPE_CHECKING

import tcod
from tcod.console import Console
from tcod.context import Context
from tcod.event import Event
from entity import Actor, Item
from game_state import GameState
from game_logic import GameLogic

if TYPE_CHECKING:
    from game_app import GameApp


class InventoryState(GameState):
    def __init__(self, game_logic: GameLogic, game_app: GameApp, parent_console: tcod.console.Console, for_actor: Actor):
        super().__init__(game_logic, game_app)
        self.width: int = 30
        self.height: int = 40
        self.this_console: tcod.console.Console = tcod.console.Console(self.width, self.height)
        self.anchor: tuple[int, int] = (parent_console.width, 0)
        self.offset: tuple[int, int] = (-self.width - 6, (parent_console.height - self.height) // 2)
        self.for_actor: Actor = for_actor
        self.items = for_actor.inventory
        self.selected_index = 0

    def render(self, parent_console: Console) -> None:
        self.this_console.draw_frame(
            0,
            0,
            self.this_console.width,
            self.this_console.height,
            decoration="┼─┼│ │┼─┼"
        )
        self.this_console.print(
            0,
            0,
            width=self.this_console.width,
            height=1,
            text=f"┤{self.for_actor.name}'s inventory├",
            alignment=tcod.constants.CENTER
        )

        cursor_x = 1
        cursor_y = 2

        if self.items:
            index = 0
            for item in self.items:
                index_str = f"({index + 1}) "
                equipped_str = f" ({str(item.equipppable.equip_slot)})" if item.equipppable and self.for_actor.is_item_equppied(item) else ""
                self.this_console.print(
                    cursor_x,
                    cursor_y,
                    text=f"{index_str}  {item.name}{equipped_str}",
                    fg=(0, 0, 0) if self.selected_index == index else (255, 255, 255),
                    bg=(255, 255, 255) if self.selected_index == index else (0, 0, 0)
                )
                self.this_console.print(
                    cursor_x + len(index_str),
                    cursor_y,
                    text=item.glyph,
                    fg=item.color
                )
                cursor_y += 1
                index += 1
        else:
            self.this_console.print(
                    cursor_x,
                    cursor_y,
                    text="<No items>"
            )

        self.this_console.blit(parent_console, self.anchor[0] + self.offset[0], self.anchor[1] + self.offset[1], bg_alpha=0.9)

    def handle_event(self, context: Context, event: Event) -> None:
        match event:
            case tcod.event.KeyDown(sym=tcod.event.KeySym.I):
                self.game_app.pop_state()
            case tcod.event.KeyDown(sym=tcod.event.KeySym.X):
                self.selected_index += 1
                if self.selected_index >= len(self.items):
                    self.selected_index = 0
            case tcod.event.KeyDown(sym=tcod.event.KeySym.W):
                self.selected_index -= 1
                if self.selected_index < 0:
                    self.selected_index = len(self.items) - 1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.RETURN):
                self.game_logic.use_item(self.for_actor, self.items[self.selected_index])
