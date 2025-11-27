from __future__ import annotations
from typing import TYPE_CHECKING

import textwrap
from typing import Tuple

import tcod
from tcod.context import Context
from tcod.event import Event

from entity import Actor, Entity, Item, EquipSlot
from game_state import GameState
from game_logic import GameLogic

if TYPE_CHECKING:
    from game_app import GameApp

class InspectState(GameState):
    def __init__(self, game_logic: GameLogic, game_app: GameApp, parent_console: tcod.console.Console, inspected_entity: Entity):
        super().__init__(game_logic, game_app)
        self.width: int = 30
        self.height: int = 40
        self.this_console: tcod.console.Console = tcod.console.Console(self.width, self.height)
        self.anchor: Tuple[int, int] = (parent_console.width, 0)
        self.offset: Tuple[int, int] = (-self.width - 6, (parent_console.height - self.height) // 2)
        self.inspected_entity: Entity = inspected_entity

    def render(self, parent_console: tcod.console.Console) -> None:
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
            text="┤Inspect├",
            alignment=tcod.constants.CENTER
        )

        cursor_x = 1
        cursor_y = 2

        name_str = f"{self.inspected_entity.name} - " 
        self.this_console.print(
            cursor_x,
            cursor_y,
            text=name_str
        )
        
        self.this_console.print(
            cursor_x + len(name_str),
            cursor_y,
            text=self.inspected_entity.glyph,
            fg=self.inspected_entity.color
        )

        cursor_y += 2

        if isinstance(self.inspected_entity, Actor) and self.inspected_entity.is_alive:
            stats = self.inspected_entity.get_modified_stats()
            self.this_console.print(
                cursor_x,
                cursor_y,
                text=f"HP: {stats.hp}/{stats.max_hp}"
            )
            cursor_y += 1
            self.this_console.print(
                cursor_x,
                cursor_y,
                text=f"Attack: {str(stats.attack)}"
            )
            cursor_y += 1
            self.this_console.print(
                cursor_x,
                cursor_y,
                text=f"Defense: {stats.defense}"
            )
            cursor_y += 2
        elif isinstance(self.inspected_entity, Item):
            if self.inspected_entity.equipppable:
                e = self.inspected_entity.equipppable
                self.this_console.print(
                    cursor_x,
                    cursor_y,
                    text=f"Equipment: {e.equip_slot}"
                )
                cursor_y += 1
                match e.equip_slot:
                    case EquipSlot.WEAPON:
                        self.this_console.print(
                            cursor_x,
                            cursor_y,
                            text=f"Attack: {e.modified_attack}"
                        )
                        cursor_y += 1
                    case EquipSlot.CHEST | EquipSlot.LEGS | EquipSlot.ARMS:
                        self.this_console.print(
                            cursor_x,
                            cursor_y,
                            text=f"Defense: {e.modified_defense}"
                        )
                        cursor_y += 1
            else:
                self.this_console.print(
                    cursor_x,
                    cursor_y,
                    text="Just an item"
                )
                cursor_y += 1
            cursor_y += 1

        self.this_console.print(
            cursor_x,
            cursor_y,
            text="Description:"
        )
        cursor_y += 2
        
        for line in self.inspected_entity.description.splitlines():
            for wrapped_line in textwrap.wrap(line, self.width - 2):
                self.this_console.print(
                    cursor_x,
                    cursor_y,
                    text=wrapped_line
                )
                cursor_y += 1
            cursor_y += 1

        self.this_console.blit(parent_console, self.anchor[0] + self.offset[0], self.anchor[1] + self.offset[1], bg_alpha=0.9)

    def handle_event(self, context: Context, event: Event) -> None:
        match event:
            case tcod.event.MouseButtonDown(button=tcod.event.MouseButton.LEFT):
                self.game_app.pop_state()
