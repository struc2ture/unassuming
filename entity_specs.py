from typing import Tuple

class EntitySpec:
    glyph: str
    color: Tuple[int, int, int]
    name: str
    description: str

    def __init__(
        self,
        glyph: str,
        color: Tuple[int, int, int],
        name: str,
        description: str
    ):
        self.glyph = glyph
        self.color = color
        self.name = name
        self.description = description


player = EntitySpec("@", (255, 255, 255), "Player", "Player Description")
crane = EntitySpec("c", (160, 30, 140), "Crane", "Crane Description")
bulb = EntitySpec("b", (30, 100, 30), "Bulb", "Bulb Description")