import tcod

from entity import Entity
from game_map import GameMap
import proc_gen

class Game:
    player: Entity
    game_map: GameMap

    def __init__(self, map_width: int, map_height: int):
        self.player = Entity("@", "Player")
        self.game_map = proc_gen.generate_map(
            max_rooms=30,
            room_min_size=6,
            room_max_size=10,
            map_width=map_width,
            map_height=map_height,
            player=self.player
        )

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
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        if self.game_map.pos_walkable(new_x, new_y):
            self.player.x = new_x
            self.player.y = new_y

    def draw(self, console: tcod.console.Console) -> None:
        self.game_map.draw(console)
        self.player.draw(console)
