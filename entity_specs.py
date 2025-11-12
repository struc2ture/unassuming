from typing import Tuple

class EntitySpec:
    glyph: str
    color: Tuple[int, int, int]
    name: str
    description: str
    is_thinking: bool

    def __init__(
        self,
        glyph: str,
        color: Tuple[int, int, int],
        name: str,
        description: str,
        is_thinking: bool
    ):
        self.glyph = glyph
        self.color = color
        self.name = name
        self.description = description
        self.is_thinking = is_thinking


player = EntitySpec("@", (255, 255, 255), "Player", "Player Description", False)
crane = EntitySpec("c", (160, 30, 140), "Crane", "Crane Description", True)
bulb = EntitySpec("b", (30, 100, 30), "Bulb", "Bulb Description", True)
