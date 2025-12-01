from dataclasses import dataclass, field

from entity import Actor
from game_intent import GameIntent

class GameEffect:
    pass

@dataclass
class StartDialogGameEffect(GameEffect):
    with_actor: Actor

@dataclass
class PickTargetGameEffect(GameEffect):
    for_intent: GameIntent
