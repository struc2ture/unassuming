from __future__ import annotations

import copy
from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Optional, Tuple, Type, TypeVar, List

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


@dataclass
class Equipment:
    weapon: Item | None = None
    chest: Item | None = None
    legs: Item | None = None
    arms: Item | None = None

    def get_modified_attack(self) -> Dice | None:
        if self.weapon and self.weapon.equipppable and self.weapon.equipppable.modified_attack:
            return self.weapon.equipppable.modified_attack
        else:
            return None
        
    def get_modified_defense(self) -> int | None:
        if self.chest and self.chest.equipppable and self.chest.equipppable.modified_defense:
            return self.chest.equipppable.modified_defense
        else:
            return None


class Actor(Entity):
    def __init__(self):
        super().__init__()

        self.stats: Stats = Stats()
        self.is_hostile: bool = False
        self.dialog: Optional[CharacterLine] = None
        self.is_alive: bool = False
        self.inventory: List[Item] = []
        self.equipment: Equipment = Equipment()

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
            inventory: List[Item] | None = None,
            equipment: Equipment | None = None
    ) -> Actor:
        template: Actor = Actor()
        template.init_common(glyph, color, name, description)
        template._render_layer = RenderLayer.ACTOR
        template.stats = stats
        template.is_hostile = is_hostile
        template.dialog = dialog
        template.is_alive = is_alive
        # TODO(A): Is 'is not None' right?
        if inventory is not None:
            template.inventory = inventory
        if equipment is not None:
            template.equipment = equipment
        return template

    def die(self) -> None:
        self.is_alive = False
        self.is_blocking = False

    def pickup_item(self, item: Item) -> None:
        self.inventory.append(item)
        item.set_in_inventory(self)

    def drop_item(self, item: Item) -> None:
        self.inventory.remove(item)
        item.set_in_world(self.x, self.y)

    def equip_item(self, item: Item) -> None:
        if item.equipppable:
            # unequipped_item = None
            match item.equipppable.equip_slot:
                case EquipSlot.WEAPON:
                    # unequipped_item = self.equipment.weapon
                    self.equipment.weapon = item
                case EquipSlot.CHEST:
                    # unequipped_item = self.equipment.chest
                    self.equipment.chest = item
                case EquipSlot.LEGS:
                    # unequipped_item = self.equipment.legs
                    self.equipment.legs = item
                case EquipSlot.ARMS:
                    # unequipped_item = self.equipment.arms
                    self.equipment.arms = item

    def is_item_equppied(self, item: Item) -> bool:
        if item.equipppable: 
                return (self.equipment.weapon == item or
                    self.equipment.chest == item or
                    self.equipment.arms == item or
                    self.equipment.legs == item)
        else:
            return False

    def get_modified_stats(self) -> Stats:
        modified_stats = Stats()
        modified_stats.hp = self.stats.hp
        modified_stats.max_hp = self.stats.max_hp
        modified_attack = self.equipment.get_modified_attack()
        modified_stats.attack = modified_attack if modified_attack else self.stats.attack
        modified_defense = self.equipment.get_modified_defense()
        modified_stats.defense = modified_defense if modified_defense else self.stats.defense
        return modified_stats

    @property
    def name(self) -> str:
        n = self._name
        if not self.is_alive:
            n += " (corpse)"
        return n

    @property
    def glyph(self) -> str:
        return self._glyph if self.is_alive else REMAINS_GLYPH

    @property
    def color(self):
        return self._color if self.is_alive else REMAINS_COLOR
    
    @property
    def render_layer(self) -> RenderLayer:
        return self._render_layer if self.is_alive else RenderLayer.CORPSE


class EquipSlot(Enum):
    WEAPON = auto()
    CHEST = auto()
    LEGS = auto()
    ARMS = auto()

    def __str__(self):
        match self:
            case EquipSlot.WEAPON:
                return "weapon"
            case EquipSlot.CHEST:
                return "chest"
            case EquipSlot.LEGS:
                return "legs"
            case EquipSlot.ARMS:
                return "arms"


@dataclass
class ItemEquippable:
    equip_slot: EquipSlot
    modified_attack: Dice | None = None
    modified_defense: int | None = None


class ItemUsable:
    # NOTE(A): TBD
    pass


class Item(Entity):
    def __init__(self):
        super().__init__()

        self.in_inventory: Actor | None = None
        self.equipppable: ItemEquippable | None = None
        self.usable: ItemUsable | None = None

    @staticmethod
    def item_template(
            glyph: str,
            color: Tuple[int, int, int],
            name: str,
            description: str,
            *,
            equippable: ItemEquippable | None = None,
            usable: ItemUsable | None = None
    ) -> Item:
        template: Item = Item()
        template.init_common(glyph, color, name, description)
        template._render_layer = RenderLayer.ITEM
        template.is_blocking = False
        template.equipppable = equippable
        template.usable = usable
        return template
    
    def get_modified_attack(self) -> Dice | None:
        if self.equipppable and self.equipppable.modified_attack:
            return self.equipppable.modified_attack
        else:
            return None
        
    def get_modified_defense(self) -> int | None:
        if self.equipppable and self.equipppable.modified_defense:
            return self.equipppable.modified_defense
        else:
            return None

    def set_in_inventory(self, actor: Actor) -> None:
        self.in_inventory = actor
        self.x = 0
        self.y = 0
    
    def set_in_world(self, x: int, y: int) -> None:
        self.in_inventory = None
        self.x = x
        self.y = y
