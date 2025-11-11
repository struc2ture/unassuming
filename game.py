import tcod

from game_map import GameMap

class Game:
    player_x: int
    player_y: int
    game_map: GameMap

    def __init__(self, map_width, map_height):
        self.game_map = GameMap(map_width, map_height)
        self.player_x = self.game_map.cols // 2
        self.player_y = self.game_map.rows // 2 

    def handle_event(self, event: tcod.event.Event) -> None:
        player_dx = 0
        player_dy = 0
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=tcod.event.KeySym.ESCAPE):
                raise SystemExit

            case tcod.event.KeyDown(sym=tcod.event.KeySym.A):
                player_dx = -1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.D):
                player_dx = +1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.W):
                player_dy = -1
            case tcod.event.KeyDown(sym=tcod.event.KeySym.S):
                player_dy = +1

        self.move_player(player_dx, player_dy)

    def move_player(self, dx, dy) -> None:
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        if self.game_map.pos_walkable(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y

    def draw(self, console: tcod.console.Console) -> None:
        self.game_map.draw(console)
        console.print(self.player_x, self.player_y, "@")
