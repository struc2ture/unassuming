from dataclasses import dataclass

from ability import Ability
from entity import Actor

@dataclass
class GameIntent:
    ability: Ability
    target: tuple[int, int] | None = None


@dataclass
class UseAbilityGameIntent(GameIntent):
    pass
