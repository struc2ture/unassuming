import textwrap
from typing import Tuple

import tcod
from tcod.context import Context
from tcod.event import Event

from entity import Actor, Entity
from game_state import GameState
from game_logic import GameLogic

class InspectState(GameState):
    def __init__(self, game_logic: GameLogic, parent_console: tcod.console.Console, inspected_entity: Entity):
        super().__init__(game_logic)
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
            text=name_str,
            fg=(255, 255, 255))
        
        self.this_console.print(
            cursor_x + len(name_str),
            cursor_y,
            text=self.inspected_entity.glyph,
            fg=self.inspected_entity.color
        )

        cursor_y += 2

        if isinstance(self.inspected_entity, Actor) and self.inspected_entity.is_alive:
            self.this_console.print(
                cursor_x,
                cursor_y,
                text=f"HP: {self.inspected_entity.stats.hp}/{self.inspected_entity.stats.max_hp}",
                fg=(255, 255, 255)
            )
            cursor_y += 1
            self.this_console.print(
                cursor_x,
                cursor_y,
                text=f"Attack: {str(self.inspected_entity.stats.attack)}",
                fg=(255, 255, 255)
            )
            cursor_y += 1
            self.this_console.print(
                cursor_x,
                cursor_y,
                text=f"Defense: {self.inspected_entity.stats.defense}",
                fg=(255, 255, 255)
            )
            cursor_y += 2

        self.this_console.print(
            cursor_x,
            cursor_y,
            text="Description:",
            fg=(255, 255, 255))
        
        cursor_y += 2
        
        for line in self.inspected_entity.description.splitlines():
            for wrapped_line in textwrap.wrap(line, self.width - 2):
                self.this_console.print(
                    cursor_x,
                    cursor_y,
                    text=wrapped_line,
                    fg=(255, 255, 255)
                )
                cursor_y += 1
            cursor_y += 1

        self.this_console.blit(parent_console, self.anchor[0] + self.offset[0], self.anchor[1] + self.offset[1], bg_alpha=0.9)

    def handle_event(self, context: Context, event: Event) -> bool:
        should_pop = False

        match event:
            case tcod.event.MouseButtonDown(button=tcod.event.MouseButton.LEFT):
                should_pop = True
                return should_pop
            
        return should_pop
