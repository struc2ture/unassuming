import tcod

class Entity:
    x: int
    y: int
    glyph: str
    name: str

    def __init__(self, glyph: str, name: str):
        self.x = 0
        self.y = 0
        self.glyph = glyph
        self.name = name

    def draw(self, console: tcod.console.Console):
        console.print(self.x, self.y, self.glyph)
