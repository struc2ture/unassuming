from typing import List

import numpy as np
import tcod

import tile_types

class TileMap:
    cols: int
    rows: int
    DEBUG_ignore_fov: bool

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.tiles = np.full((cols, rows), fill_value=tile_types.wall, order="F")
        self.visible = np.full((cols, rows), fill_value=False, order="F")
        self.explored = np.full((cols, rows), fill_value=False, order="F")
        self.DEBUG_ignore_fov = False

    def pos_in_bounds(self, x, y) -> bool:
        return (
            x >= 0 and x < self.cols and
            y >= 0 and y < self.rows
        )

    def pos_walkable(self, x, y) -> bool:
        return (
            self.pos_in_bounds(x, y) and
            self.tiles["walkable"][x, y] == 1
        )

    def pos_visible(self, x, y) -> bool:
        return self.DEBUG_ignore_fov or self.visible[x, y] == 1
    
    def DEBUG_toggle_ignore_fov(self):
        self.DEBUG_ignore_fov = not self.DEBUG_ignore_fov

    def draw(self, console: tcod.console.Console):
        if not self.DEBUG_ignore_fov:
            console.rgb[0:self.cols, 0:self.rows] = np.select(
                condlist=[self.visible, self.explored],
                choicelist=[self.tiles["light"], self.tiles["dark"]],
                default=tile_types.SHROUD
            )
        else:
            console.rgb[0:self.cols, 0:self.rows] = self.tiles["light"]
