import tcod

from game_logic import GameLogic

class GameState:
    game_logic: GameLogic

    def __init__(self, game_logic: GameLogic):
        self.game_logic = game_logic

    def render(self, parent_console: tcod.console.Console) -> None:
        pass

    def handle_event(self, context: tcod.context.Context, event: tcod.event.Event) -> bool:
        return False

