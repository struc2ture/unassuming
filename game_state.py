from __future__ import annotations
from typing import TYPE_CHECKING

import tcod

from game_logic import GameLogic

if TYPE_CHECKING:
    from game_app import GameApp

class GameState:
    game_logic: GameLogic
    game_app: GameApp

    def __init__(self, game_logic: GameLogic, game_app: GameApp):
        self.game_logic = game_logic
        self.game_app = game_app

    def render(self, parent_console: tcod.console.Console) -> None:
        pass

    def handle_event(self, context: tcod.context.Context, event: tcod.event.Event) -> None:
        pass
