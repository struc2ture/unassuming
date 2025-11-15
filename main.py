import traceback

import tcod

from game_app import GameApp


def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        "Taffer_20x20.png", 16, 16, tcod.tileset.CHARMAP_CP437
    )
    tcod.tileset.procedural_block_elements(tileset=tileset)
    console = tcod.console.Console(80, 50, order="F")

    game = GameApp(80, 50, console)

    with tcod.context.new(console=console, tileset=tileset, title="Unassuming") as context:
        while True:  # Main loop
            for event in tcod.event.wait():  # Event loop, blocks until pending events exist
                game.handle_event(context, event)
            
            console.clear()
            game.draw(console)
            context.present(console)  # Render the console to the window and show it


if __name__ == "__main__":
    main()
