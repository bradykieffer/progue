import random
from progue.tiles import *

# Maxmimum values for tiles to appear
THRESHOLDS = {
    TILE_GROUND: 0.75,
    TILE_WATER: 0.0,
    TILE_SAND: 0.2,
    TILE_WALL: 1.0  # For now this is unused
}


class Chunk(object):

    def __init__(self, num, width, height):
        self.num = num
        self.width = width
        self.height = height
        self.raw_map = []
        self.map = []


    def tile_num_map(self, num):
        if num < THRESHOLDS[TILE_WATER]:
            return TILES[TILE_WATER][random.randint(0, len(TILES[TILE_WATER]) - 1)]

        elif num < THRESHOLDS[TILE_SAND]:
            return TILES[TILE_SAND]

        elif num < THRESHOLDS[TILE_GROUND]:
            return TILES[TILE_GROUND]

        else:
            return TILES[TILE_WALL]
        """
        return TILES[TILE_DEBUG]
        """

    def create_tile_map(self):
        for j in xrange(len(self.raw_map)):
            self.map.append([])
            for i in xrange(len(self.raw_map[j])):
                self.map[j].append(self.tile_num_map(self.raw_map[j][i]))

    def tile_at(self, x, y):
        if self.in_bounds(x, y):
            return self.map[y][x]
        return None

    def in_bounds(self, x, y):
        if x >= 0 and y >= 0 and x < self.width and y < self.height:
            return True
        return False
