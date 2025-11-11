from typing import List, Optional

from game_map import GameMap
from entity import Entity

class EntityController:
    game_map: GameMap
    entities: List[Entity]
    def __init__(self, game_map: GameMap, entities: List[Entity]):
        self.game_map = game_map
        self.entities = entities

    def get_entity_at(self, x: int, y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return entity
        
        return None

    def move(self, entity: Entity, dx: int, dy: int) -> None:
        new_x = entity.x + dx
        new_y = entity.y + dy
        if (
            self.game_map.pos_walkable(new_x, new_y) and
            self.get_entity_at(new_x, new_y) is None
        ):
            entity.set_pos(new_x, new_y)

    def move_or_bump(self, entity: Entity, dx: int, dy: int) -> None:
        new_x = entity.x + dx
        new_y = entity.y + dy
        if self.game_map.pos_walkable(new_x, new_y):
            bumped_entity = self.get_entity_at(new_x, new_y)
            if bumped_entity is None or bumped_entity is entity:
                entity.set_pos(new_x, new_y)
            else:
                print(f'{entity.spec.name} bumps against {bumped_entity.spec.name}')
