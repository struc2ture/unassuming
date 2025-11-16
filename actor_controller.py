from dataclasses import dataclass

from entity import Actor
from game_logic import GameLogic

@dataclass
class ActorController:
    game_logic: GameLogic

    def hostile_ai_turn(self, actor: Actor):
        target_entity = self.game_logic.player
        # NOTE(A): This is if PLAYER sees the acting actor (for now)
        if self.game_logic.tile_map.visible[actor.x, actor.y]:
            path = self.game_logic.get_path_to(actor, *target_entity.pos)
            if path:
                next_step = path.pop(0)
                self.game_logic.entity_move_or_bump(actor, *next_step)

    def friendly_ai_turn(self, actor: Actor):
        pass

    def process_actor_turn(self, actor: Actor):
        if actor.is_hostile:
            self.hostile_ai_turn(actor)
        else:
            self.friendly_ai_turn(actor)
