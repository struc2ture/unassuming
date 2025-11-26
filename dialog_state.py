from __future__ import annotations
from typing import TYPE_CHECKING

import textwrap
from typing import List, Tuple

import tcod

from dialog import CharacterLine, PlayerLine
from entity import Actor
from game_state import GameState
from game_logic import GameLogic
from trading_state import TradingState

if TYPE_CHECKING:
    from game_app import GameApp

class DialogState(GameState):
    dialog_text: str
    options: List[Tuple[str, CharacterLine | None]]
    pending_action: str | None

    def __init__(self, game_logic: GameLogic, game_app: GameApp, parent_console: tcod.console.Console, with_actor: Actor):
        super().__init__(game_logic, game_app)
        self.width: int = 30
        self.height: int = 40
        self.this_console = tcod.console.Console(self.width, self.height)
        self.parent_console = parent_console
        self.anchor: Tuple[int, int] = (parent_console.width, 0)
        self.offset: Tuple[int, int] = (-self.width - 6, (parent_console.height - self.height) // 2)
        self.with_actor: Actor = with_actor
        self.set_character_line(self.with_actor.dialog)
        self.selected_choice = -1

    def set_character_line(self, character_line: CharacterLine | None):
        if character_line:
            self.dialog_text = character_line.text
            self.pending_action = character_line.action
            if character_line.responses:
                self.options = []
                for player_line in character_line.responses:
                    if player_line.text == "<Continue>":
                        self.options.append((player_line.text, character_line.next_line))
                    else:
                        self.options.append((player_line.text, player_line.character_line))
            elif character_line.next_line:
                self.options = [("<Continue>", character_line.next_line)]
            else:
                self.options = [("<Quit>", None)]
        else:
            self.dialog_text = "{NO LINE}"
            self.options = [("<Quit>", None)]

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

        # Print character's line
        for line in self.dialog_text.splitlines():
            for wrapped_line in textwrap.wrap(line, self.width - 2):
                self.this_console.print(
                    cursor_x,
                    cursor_y,
                    text=wrapped_line,
                    fg=(255, 255, 255)
                )
                cursor_y += 1
            cursor_y += 1
        
        # Print player's choices
        choice_i = 1
        for choice in self.options:
            first_wrapped_line = True
            for wrapped_line in textwrap.wrap(choice[0], self.width - 6):
                if first_wrapped_line:
                    text = f"({choice_i}) {wrapped_line}"
                else:
                    text = f"    {wrapped_line}"

                self.this_console.print(
                    cursor_x,
                    cursor_y,
                    text=text,
                    fg=(255, 255, 255)
                )
                first_wrapped_line = False
                cursor_y += 1

            cursor_y += 1
            choice_i += 1

        self.this_console.blit(parent_console, self.anchor[0] + self.offset[0], self.anchor[1] + self.offset[1], bg_alpha=0.9)

    def handle_event(self, context: tcod.context.Context, event: tcod.event.Event) -> None:
        match event:
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N1):
                self.selected_choice = 0
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N2):
                self.selected_choice = 1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N3):
                self.selected_choice = 2
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N4):
                self.selected_choice = 3
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N5):
                self.selected_choice = 4
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N6):
                self.selected_choice = 5
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N7):
                self.selected_choice = 6
            case tcod.event.KeyDown(sym=tcod.event.KeySym.N8):
                self.selected_choice = 7

        if 0 <= self.selected_choice < len(self.options):
            match self.pending_action:
                case "turn_hostile":
                    self.game_logic.turn_actor_hostile(self.with_actor)
                    self.pending_action = None
                case "start_trade":
                    self.game_app.push_state(TradingState(self.game_logic, self.game_app, self.parent_console, self.game_logic.player, self.with_actor))
                    self.pending_action = None
                    return

            if self.options[self.selected_choice][1]:
                self.set_character_line(self.options[self.selected_choice][1])
                self.selected_choice = -1
            else:
                self.game_app.pop_state()
