import tcod

class GameState:
    def render(self, console: tcod.console.Console) -> None:
        pass

    def handle_event(self, context: tcod.context.Context, event: tcod.event.Event) -> bool:
        should_pop = True
        return should_pop
