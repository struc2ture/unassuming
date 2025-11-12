from typing import Tuple

class EntitySpec:
    glyph: str
    color: Tuple[int, int, int]
    name: str
    description: str
    is_thinking: bool
    max_health: int
    attack: int
    defense: int

    def __init__(
        self,
        glyph: str,
        color: Tuple[int, int, int],
        name: str,
        description: str,
        is_thinking: bool,
        max_health: int,
        attack: int,
        defense: int
    ):
        self.glyph = glyph
        self.color = color
        self.name = name
        self.description = description
        self.is_thinking = is_thinking
        self.max_health = max_health
        self.attack = attack
        self.defense = defense


player = EntitySpec("@", (255, 255, 255), "Player", "Player Description", False, 10, 2, 1)
crane = EntitySpec("c", (160, 30, 140), "Crane", "Crane Description", True, 3, 1, 1)
bulb = EntitySpec("b", (30, 100, 30), "Bulb", "Bulb Description", True, 15, 3, 3)
