from __future__ import annotations

import copy
from enum import auto, Enum
from typing import Optional, Tuple, Type, TypeVar

import tcod

T = TypeVar("T", bound="Entity")

class RenderLayer(Enum):
    DEFAULT = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()

class Entity:
    def __init__(self):
        self.x: int = 0
        self.y: int = 0

        self.glyph: str = "0"
        self.color: Tuple[int, int, int] = (255, 0, 0)
        self.render_layer = RenderLayer.DEFAULT

        self._name: str = "<Unnamed>"
        self.description: str = "<Undescribed>"

        self.is_blocking: bool = False

        self.copy_source: Optional[Entity] = None

    @property
    def name(self):
        return self._name

    @staticmethod
    def entity_template(glyph: str, color: Tuple[int, int, int], name: str, description: str) -> Entity:
        template: Entity = Entity()
        template.init_common(glyph, color, name, description)
        return template
    
    def init_common(self, glyph: str, color: Tuple[int, int, int], name: str, description: str):
        self.glyph = glyph
        self.color = color
        self._name = name
        self.description = description
        self.is_blocking = True

    def spawn(self: T, x: int, y: int) -> T:
        spawned_entity: T = copy.deepcopy(self)
        spawned_entity.set_pos(x, y)
        spawned_entity.copy_source = self
        return spawned_entity

    @property
    def pos(self) -> Tuple[int, int]:
        return self.x, self.y

    def set_pos(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self, console: tcod.console.Console) -> None:
        glyph = self.glyph
        color = self.color
        console.print(
            x=self.x,
            y=self.y,
            text=glyph,
            fg=color
        )


class Stats:
    def __init__(
            self,
            hp: int = 0,
            max_hp: int = 0,
            attack: int = 0,
            defense: int = 0
    ):
        self.hp: int = hp
        self.max_hp: int = max_hp
        self.attack: int = attack
        self.defense: int = defense

REMAINS_GLYPH = "%"
REMAINS_COLOR = (150, 30, 30)

class Actor(Entity):
    def __init__(self):
        super().__init__()

        self.stats: Stats = Stats()
        self.is_alive: bool = False

    @staticmethod
    def actor_template(
            glyph: str,
            color: Tuple[int, int, int],
            name: str,
            description: str,
            stats: Stats,
            is_alive: bool = True
    ) -> Actor:
        template: Actor = Actor()
        template.init_common(glyph, color, name, description)
        template.render_layer = RenderLayer.ACTOR
        template.stats = stats
        template.is_alive = is_alive
        return template

    def die(self):
        self.is_alive = False
        self.is_blocking = False
        # NOTE(A): It feels off to set it here.
        #          If remains' glyph and color is handled with the is_alive flag,
        #          it feels like the 'renderer' should handle the render order with that flag too.
        #          But I don't handle render order inside the Entity.draw, so I will keep this logic for now.
        self.render_layer = RenderLayer.CORPSE

    @property
    def name(self):
        n = self._name
        if not self.is_alive:
            n += " (corpse)"
        return n

    def draw(self, console: tcod.console.Console) -> None:
        glyph = self.glyph if self.is_alive else REMAINS_GLYPH
        color = self.color if self.is_alive else REMAINS_COLOR
        console.print(
            x=self.x,
            y=self.y,
            text=glyph,
            fg=color
        )
