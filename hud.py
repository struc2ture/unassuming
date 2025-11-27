import tcod

from game_logic import GameLogic
from in_game_log import InGameLog

class Hud:
    def __init__(self, x: int, y: int, width: int, height: int, game_logic: GameLogic):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.console = tcod.console.Console(self.width, self.height)
        self.game_logic = game_logic
        self.DEBUG_enable_hud = True

    def draw_player_health(self) -> None:
        self.console.draw_rect(
            0,
            0,
            self.width,
            1,
            ch=0,
            bg=(200, 50, 50)
        )
        self.console.draw_rect(
            0,
            0,
            int((self.game_logic.player.stats.hp / self.game_logic.player.stats.max_hp) * self.width),
            1,
            ch=0,
            bg=(50, 200, 50)
        )
        self.console.print(
            0,
            0,
            width=self.width,
            height=1,
            text=f"Player Health",
            alignment=tcod.constants.CENTER
        )

    def draw_in_game_log(self) -> None:
        self.console.draw_frame(
            0,
            1,
            self.width,
            5,
            decoration="         ",
            bg=(0, 0, 0)
        )
        cursor_x = 0
        cursor_y = 1
        for message in InGameLog.log.messages[-5:]:
            self.console.print(
                cursor_x,
                cursor_y,
                text=message,
            )
            cursor_y += 1

    def DEBUG_toggle_hud(self):
        self.DEBUG_enable_hud = not self.DEBUG_enable_hud

    def draw_hud(self, parent_console: tcod.console.Console):
        if self.DEBUG_enable_hud:
            self.draw_player_health()
            self.draw_in_game_log()
            self.console.blit(parent_console, self.x, self.y, bg_alpha=0.9)
