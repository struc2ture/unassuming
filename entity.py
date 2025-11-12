from typing import Tuple

import tcod

from entity_specs import EntitySpec

class Entity:
    spec: EntitySpec
    x: int
    y: int
    health: int
    is_alive: bool
    is_remains: bool

    def __init__(self, spec: EntitySpec, x: int, y: int):
        self.spec = spec
        self.x = x
        self.y = y
        self.health = self.spec.max_health
        self.is_alive = self.health > 0
        self.is_remains = False

    @property
    def pos(self) -> Tuple[int, int]:
        return self.x, self.y

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def is_blocking(self) -> bool:
        return not self.is_remains

    def draw(self, console: tcod.console.Console) -> None:
        # NOTE(A): A temporary way of displaying remains

        glyph = self.spec.glyph if not self.is_remains else "%"
        color = self.spec.color if not self.is_remains else (140, 20, 20)
        console.print(
            x=self.x,
            y=self.y,
            text=glyph,
            fg=color
        )
