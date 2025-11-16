from dataclasses import dataclass, field

from entity import Actor

class GameEffect:
    pass

@dataclass
class StartDialogGameEffect(GameEffect):
    with_actor: Actor
