from typing import Tuple

import tcod

from entity_specs import EntitySpec

class Entity:
    spec: EntitySpec
    x: int
    y: int
    health: int

    def __init__(self, spec: EntitySpec, x: int, y: int):
        self.spec = spec
        self.x = x
        self.y = y
        self.health = self.spec.max_health

    @property
    def pos(self) -> Tuple[int, int]:
        return self.x, self.y

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self, console: tcod.console.Console) -> None:
        console.print(
            x=self.x,
            y=self.y,
            text=self.spec.glyph,
            fg=self.spec.color
        )
