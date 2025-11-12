from typing import List, Tuple, Optional

import numpy as np
import tcod

from game_map import GameMap
from entity import Entity

class EntityController:
    game_map: GameMap
    entities: List[Entity]
    player: Entity

    def __init__(self, game_map: GameMap, entities: List[Entity], player: Entity):
        self.game_map = game_map
        self.entities = entities
        self.player = player

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

    def bump(self, entity: Entity, bumped_entity: Entity) -> None:
        damage = min(bumped_entity.spec.defense - entity.spec.attack, bumped_entity.health)
        bumped_entity.health -= damage

        print(f'{entity.spec.name} bumps against {bumped_entity.spec.name}, dealing {damage} damage')
        if bumped_entity.health <= 0:
            print(f'{bumped_entity.spec.name} is dead.')

    def skip_turn(self, entity: Entity) -> None:
        pass

    def move_or_bump(self, entity: Entity, dx: int, dy: int) -> None:
        new_x = entity.x + dx
        new_y = entity.y + dy
        if self.game_map.pos_walkable(new_x, new_y):
            bumped_entity = self.get_entity_at(new_x, new_y)
            if bumped_entity and bumped_entity is not entity:
                self.bump(entity, bumped_entity)
            else:
                entity.set_pos(new_x, new_y)

    def teleport_or_bump(self, entity: Entity, x: int, y: int) -> None:
        bumped_entity = self.get_entity_at(x, y)
        if bumped_entity and bumped_entity is not entity:
                self.bump(entity, bumped_entity)
        else:
            entity.set_pos(x, y)

    def get_path_to(self, entity: Entity, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        cost = np.array(self.game_map.tiles["walkable"], dtype=np.int8)

        # NOTE(A): Cost = 0 means the tile is completely blocked.
        # Walkable tiles have cost = 1 -- the minimum cost.
        # Rank tiles with blocking entities as walkable, but higher cost.
        # A tile with an entity should not be considered completely blocked,
        # that would mean that an a player surrounded by two entities in a corridor
        # is unreachable, and everyone else would stop following the player.
        # But a tile with an entity should have a higher cost, so that enemies are
        # "smarter" -- they will try to walk around, and reach the player from the other side,
        # not just stand there and wait for the enemy in front of them to move.
        # Higher cost means an enemy will go to greater lengths to walk around to get to the player.
        # Lower cost means they will walk around only if there's a short path to get to the player.
        entity_tile_cost = 10
        
        # For every tile with a blocking entity on top of it, set its rank to be higher cost
        for blocking_entity in self.entities:
            if cost[blocking_entity.x, blocking_entity.y]:
                cost[blocking_entity.x, blocking_entity.y] += entity_tile_cost

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((entity.x, entity.y)) # Start position

        #TODO(A): Do we need to hang on to the whole path?

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]]
        return [(index[0], index[1]) for index in path]

    def think_and_act_for(self, entity: Entity):
        target_entity = self.player
        # NOTE(A): This is if PLAYER sees the acting entity (for now)
        if self.game_map.visible[entity.x, entity.y]:
            path = self.get_path_to(entity, *target_entity.pos)
            if path:
                next_step = path.pop(0)
                self.teleport_or_bump(entity, *next_step)

    def process_entities_turns(self):
        for entity in self.entities:
            if entity.spec.is_thinking:
                self.think_and_act_for(entity)
