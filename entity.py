import tcod

from game_map import GameMap

class Entity:
    x: int
    y: int
    glyph: str
    name: str

    def __init__(self, glyph: str, name: str):
        self.glyph = glyph
        self.name = name

    def set_pos(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def draw(self, console: tcod.console.Console) -> None:
        console.print(self.x, self.y, self.glyph)
