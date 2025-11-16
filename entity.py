from __future__ import annotations

import copy
from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Optional, Tuple, Type, TypeVar

import tcod

from dialog import CharacterLine
from dice import Dice

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

        self._glyph: str = "0"
        self._color: Tuple[int, int, int] = (255, 0, 0)
        self._render_layer = RenderLayer.DEFAULT

        self._name: str = "<Unnamed>"
        self.description: str = "<Undescribed>"

        self.is_blocking: bool = False

        self.copy_source: Optional[Entity] = None

    @property
    def name(self):
        return self._name
    
    @property
    def glyph(self):
        return self._glyph
    
    @property
    def color(self):
        return self._color
    
    @property
    def render_layer(self):
        return self._render_layer

    @staticmethod
    def entity_template(glyph: str, color: Tuple[int, int, int], name: str, description: str) -> Entity:
        template: Entity = Entity()
        template.init_common(glyph, color, name, description)
        return template
    
    def init_common(self, glyph: str, color: Tuple[int, int, int], name: str, description: str):
        self._glyph = glyph
        self._color = color
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

@dataclass
class Stats:
    hp: int = 0
    max_hp: int = 0
    attack: Dice = field(default_factory=lambda: Dice())
    defense: int = 0

REMAINS_GLYPH = "%"
REMAINS_COLOR = (150, 30, 30)

class Actor(Entity):
    def __init__(self):
        super().__init__()

        self.stats: Stats = Stats()
        self.is_hostile: bool = False
        self.dialog: Optional[CharacterLine] = None
        self.is_alive: bool = False

    @staticmethod
    def actor_template(
            glyph: str,
            color: Tuple[int, int, int],
            name: str,
            description: str,
            stats: Stats,
            *,
            is_hostile: bool = True,
            dialog: Optional[CharacterLine] = None,
            is_alive: bool = True,
    ) -> Actor:
        template: Actor = Actor()
        template.init_common(glyph, color, name, description)
        template._render_layer = RenderLayer.ACTOR
        template.stats = stats
        template.is_hostile = is_hostile
        template.dialog = dialog
        template.is_alive = is_alive
        return template

    def die(self):
        self.is_alive = False
        self.is_blocking = False

    @property
    def name(self):
        n = self._name
        if not self.is_alive:
            n += " (corpse)"
        return n

    @property
    def glyph(self):
        return self._glyph if self.is_alive else REMAINS_GLYPH

    @property
    def color(self):
        return self._color if self.is_alive else REMAINS_COLOR
    
    @property
    def render_layer(self):
        return self._render_layer if self.is_alive else RenderLayer.CORPSE
