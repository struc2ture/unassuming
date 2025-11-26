from typing import List, Tuple, Optional

import numpy as np
import tcod

from tile_map import TileMap
from game_trace import GameTrace
from game_effect import GameEffect, StartDialogGameEffect
from entity import Actor, Entity, Item
import proc_gen
import templates

class GameLogic:
    tile_map: TileMap
    entities: List[Entity]
    player: Actor

    def __init__(self, map_width: int, map_height: int):
        self.player = templates.PLAYER.spawn(0, 0)
        self.entities = [self.player]

        map_spec = proc_gen.MapSpec(
            max_rooms=30,
            room_min_size=6,
            room_max_size=10,
            map_width=map_width,
            map_height=map_height,
            max_monsters_per_room=2
        )
        self.tile_map = proc_gen.generate_map(
            map_spec,
            player=self.player,
            entities=self.entities
        )

        self.update_fov()

    def get_entities_at(self, x: int, y: int) -> List[Entity]:
        result = []
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                if not isinstance(entity, Item) or not entity.in_inventory:
                    result.append(entity)
        return result
    
    def get_blocking_entity_at(self, x: int, y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                if entity.is_blocking:
                    return entity
        return None

    def move(self, entity: Entity, x: int, y: int) -> None:
        log_entry = GameTrace.log.add_entry("MOVE")
        log_entry.add_item(f"entity: {entity.name}")
        log_entry.add_item(f"from: {entity.pos}")

        entity.set_pos(x, y)

        log_entry.add_item(f"to: {entity.pos}")

    def attack(self, attacker: Actor, defender: Actor) -> None:
        entry = GameTrace.log.add_entry("ATTACK")
        entry.add_item(f"attacker: {attacker.name} ({attacker.stats.hp}/{attacker.stats.max_hp} HP)")
        entry.add_item(f"defender: {defender.name} ({defender.stats.hp}/{defender.stats.max_hp} HP)")

        modified_attack_dice = attacker.stats.attack
        if attacker.equipment.weapon and attacker.equipment.weapon.equipppable and attacker.equipment.weapon.equipppable.modified_attack:
            modified_attack_dice = attacker.equipment.weapon.equipppable.modified_attack
            entry.add_item(f"attacker_weapon: {attacker.equipment.weapon.name}; modified_attack: {attacker.equipment.weapon.equipppable.modified_attack}")
        else:
            entry.add_item(f"attacker_weapon: none; base_attack: {modified_attack_dice}")

        modified_defense = defender.stats.defense
        if defender.equipment.chest and defender.equipment.chest.equipppable and defender.equipment.chest.equipppable.modified_defense:
            modified_defense = defender.equipment.chest.equipppable.modified_defense
            entry.add_item(f"defender_chest_piece: {defender.equipment.chest.name}; modified_defense: {defender.equipment.chest.equipppable.modified_defense}")
        else:
            entry.add_item(f"defender_chest_piece: none; base_defense: {modified_defense}")

        attack_roll = modified_attack_dice.roll()

        entry.add_item(f"attack_roll: {modified_attack_dice} -> {attack_roll}")
        entry.add_item(f"defense: {modified_defense}")

        damage = min(max(attack_roll - modified_defense, 0), defender.stats.hp)
        entry.add_item(f"damage: {damage}")
        defender.stats.hp -= damage
        if defender.stats.hp <= 0:
            defender.die()
            entry.add_item(f"defender_died: true")

        log_line = f'{attacker.name} swings at {defender.name}, '
        log_line += f'and deals {damage} damage' if damage > 0 else 'but misses'
        log_line += '.' if defender.is_alive else ', killing them.'
        print(log_line)

    def bump(self, entity: Entity, bumped_entity: Entity) -> List[GameEffect]:
        if isinstance(entity, Actor) and isinstance(bumped_entity, Actor):
            if entity is self.player and not bumped_entity.is_hostile:
                if bumped_entity.dialog:
                    return [StartDialogGameEffect(bumped_entity)]
            else:
                self.attack(entity, bumped_entity)
        return []

    def skip_turn(self, entity: Entity) -> None:
        pass

    def pickup_item_below(self, actor: Actor) -> None:
        for entity in self.get_entities_at(actor.x, actor.y):
            if isinstance(entity, Item):
                actor.pickup_item(entity)
                return
            
    def drop_item(self, actor: Actor) -> None:
        if actor.inventory:
            actor.drop_item(actor.inventory[0])

    def turn_actor_hostile(self, actor: Actor) -> None:
        actor.is_hostile = True

    def player_move_or_bump(self, entity: Entity, dx: int, dy: int) -> List[GameEffect]:
        new_x = entity.x + dx
        new_y = entity.y + dy
        if self.tile_map.pos_walkable(new_x, new_y):
            bumped_entity = self.get_blocking_entity_at(new_x, new_y)
            if bumped_entity and bumped_entity is not entity:
                return self.bump(entity, bumped_entity)
            else:
                self.move(entity, new_x, new_y)
        self.update_fov()
        return []

    def entity_move_or_bump(self, entity: Entity, x: int, y: int) -> None:
        bumped_entity = self.get_blocking_entity_at(x, y)
        if bumped_entity and bumped_entity is not entity:
                self.bump(entity, bumped_entity)
        else:
            self.move(entity, x, y)

    def use_item(self, actor: Actor, item: Item) -> list[GameEffect]:
        if item.equipppable:
            actor.equip_item(item)
        return []

    def trade_items(self, actor_a: Actor, actor_b: Actor, item_a: Item, item_b: Item) -> None:
        actor_a.inventory.remove(item_a)
        actor_b.inventory.remove(item_b)
        actor_a.inventory.append(item_b)
        actor_b.inventory.append(item_a)
        item_a.set_in_inventory(actor_b)
        item_b.set_in_inventory(actor_a)

    def get_path_to(self, entity: Entity, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        cost = np.array(self.tile_map.tiles["walkable"], dtype=np.int8)

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
    
    def update_fov(self) -> None:
        self.tile_map.visible[:] = tcod.map.compute_fov(
            self.tile_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        self.tile_map.explored |= self.tile_map.visible
