import textwrap
from typing import Tuple

import tcod
from dialog import CharacterLine
from game_state import GameState

class DialogState(GameState):
    def __init__(self, parent_console: tcod.console.Console, character_line: CharacterLine):
        self.width: int = 30
        self.height: int = 40
        self.this_console = tcod.console.Console(self.width, self.height)
        self.anchor: Tuple[int, int] = (parent_console.width, 0)
        self.offset: Tuple[int, int] = (-self.width - 6, (parent_console.height - self.height) // 2)
        self.character_line: CharacterLine = character_line

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
            text="┤Dialog├",
            alignment=tcod.constants.CENTER
        )

        cursor_x = 1
        cursor_y = 2

        for line in self.character_line.text.splitlines():
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

    def handle_event(self, context: tcod.context.Context, event: tcod.event.Event) -> bool:
        return super().handle_event(context, event)
